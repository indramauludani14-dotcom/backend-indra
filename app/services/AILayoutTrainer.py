"""
AI Layout Trainer - Machine Learning untuk Auto Layout Furniture
Menggunakan Random Forest untuk prediksi posisi optimal
"""

import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, List, Tuple
import json

class AILayoutTrainer:
    """Train AI model untuk furniture placement"""
    
    # Layout dimensions (meters)
    ROOM_WIDTH = 17.0
    ROOM_HEIGHT = 11.0
    
    # Zones definition
    ZONES = {
        "living": {"x_min": 1.0, "x_max": 7.5, "y_min": 1.0, "y_max": 5.5},
        "dining": {"x_min": 9.0, "x_max": 15.5, "y_min": 1.0, "y_max": 5.5},
        "outdoor": {"x_min": 1.5, "x_max": 15.5, "y_min": 7.0, "y_max": 9.5},
        "decoration": {"x_min": 1.0, "x_max": 16.0, "y_min": 1.0, "y_max": 10.0}
    }
    
    # Obstacles (tangga dan kolom)
    OBSTACLES = [
        {"name": "Tangga Up L1", "x": 12.4, "y": 1.6, "width": 1.6, "height": 2.8},
        {"name": "Tangga Down L2", "x": 9.0, "y": 7.6, "width": 2.0, "height": 1.6},
        {"name": "Tangga Up L2", "x": 11.6, "y": 7.6, "width": 2.0, "height": 1.6},
        {"name": "Column 1", "x": 8.5, "y": 5.0, "width": 0.36, "height": 0.36},
        {"name": "Column 2", "x": 15.0, "y": 5.0, "width": 0.36, "height": 0.36},
        {"name": "Column 3", "x": 8.5, "y": 6.5, "width": 0.36, "height": 0.36},
        {"name": "Column 4", "x": 15.0, "y": 6.5, "width": 0.36, "height": 0.36}
    ]
    
    # Spacing rules
    MIN_SPACING = 0.6  # 60cm between furniture
    WALL_MARGIN = 0.4  # 40cm from walls
    OBSTACLE_MARGIN = 0.5  # 50cm from obstacles
    
    # Furniture catalog
    FURNITURE_CATALOG = {
        "SOFA 3 Seat": {"panjang": 2.6, "lebar": 1.0, "zone": "living", "quantity": 4, "priority": 1},
        "SOFA 1 Seat": {"panjang": 1.14, "lebar": 1.0, "zone": "living", "quantity": 4, "priority": 2},
        "Meja Makan": {"panjang": 2.4, "lebar": 1.0, "zone": "dining", "quantity": 4, "priority": 3},
        "Kursi Makan": {"panjang": 0.46, "lebar": 0.75, "zone": "dining", "quantity": 24, "priority": 8},
        "Lemari Piring": {"panjang": 1.2, "lebar": 0.6, "zone": "dining", "quantity": 2, "priority": 5},
        "Lukisan Besar": {"panjang": 4.0, "lebar": 1.5, "zone": "decoration", "quantity": 1, "priority": 4},
        "Lukisan Kecil": {"panjang": 0.6, "lebar": 0.6, "zone": "decoration", "quantity": 3, "priority": 9},
        "Stand Lukisan": {"panjang": 0.6, "lebar": 0.75, "zone": "decoration", "quantity": 3, "priority": 10},
        "Meja Teras": {"panjang": 2.4, "lebar": 1.0, "zone": "outdoor", "quantity": 2, "priority": 6},
        "Kursi Teras": {"panjang": 0.46, "lebar": 0.75, "zone": "outdoor", "quantity": 8, "priority": 11},
        "Rak Display": {"panjang": 2.0, "lebar": 0.5, "zone": "decoration", "quantity": 2, "priority": 7},
        "Pot Bunga Small": {"panjang": 0.36, "lebar": 0.36, "zone": "decoration", "quantity": 4, "priority": 12},
        "Pot Bunga Medium": {"panjang": 0.43, "lebar": 0.43, "zone": "decoration", "quantity": 3, "priority": 13},
        "Pot Bunga Large": {"panjang": 0.6, "lebar": 0.6, "zone": "decoration", "quantity": 3, "priority": 14},
        "Standing AC": {"panjang": 0.5, "lebar": 0.4, "zone": "living", "quantity": 2, "priority": 15}
    }
    
    @staticmethod
    def check_collision(x1: float, y1: float, w1: float, h1: float,
                       x2: float, y2: float, w2: float, h2: float,
                       spacing: float = 0.6) -> bool:
        """Check AABB collision with spacing"""
        return not (x1 + w1 + spacing < x2 or 
                   x2 + w2 + spacing < x1 or 
                   y1 + h1 + spacing < y2 or 
                   y2 + h2 + spacing < y1)
    
    @staticmethod
    def is_valid_position(x: float, y: float, panjang: float, lebar: float,
                         zone_name: str, placed_items: List[Dict]) -> bool:
        """Check if position is valid (no collision, within zone)"""
        
        # Check zone boundaries
        zone = AILayoutTrainer.ZONES.get(zone_name)
        if not zone:
            return False
        
        margin = AILayoutTrainer.WALL_MARGIN
        if not (x >= zone["x_min"] + margin and 
                x + panjang <= zone["x_max"] - margin and
                y >= zone["y_min"] + margin and 
                y + lebar <= zone["y_max"] - margin):
            return False
        
        # Check obstacle collision
        for obstacle in AILayoutTrainer.OBSTACLES:
            if AILayoutTrainer.check_collision(
                x, y, panjang, lebar,
                obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"],
                spacing=AILayoutTrainer.OBSTACLE_MARGIN
            ):
                return False
        
        # Check collision with placed furniture
        for item in placed_items:
            if AILayoutTrainer.check_collision(
                x, y, panjang, lebar,
                item["x"], item["y"], item["panjang"], item["lebar"],
                spacing=AILayoutTrainer.MIN_SPACING
            ):
                return False
        
        return True
    
    @staticmethod
    def calculate_position_features(x: float, y: float, panjang: float, lebar: float,
                                   zone_name: str, placed_items: List[Dict],
                                   furniture_type: str) -> List[float]:
        """Calculate features for machine learning"""
        zone = AILayoutTrainer.ZONES.get(zone_name)
        
        # Basic position features
        features = [
            x, y, panjang, lebar,
            x + panjang, y + lebar,  # Bottom right corner
            x + panjang/2, y + lebar/2,  # Center point
        ]
        
        # Zone features
        zone_center_x = (zone["x_min"] + zone["x_max"]) / 2
        zone_center_y = (zone["y_min"] + zone["y_max"]) / 2
        features.extend([
            abs(x - zone_center_x),  # Distance from zone center X
            abs(y - zone_center_y),  # Distance from zone center Y
            zone["x_max"] - zone["x_min"],  # Zone width
            zone["y_max"] - zone["y_min"],  # Zone height
        ])
        
        # Distance to nearest obstacle
        min_obstacle_dist = 999
        for obstacle in AILayoutTrainer.OBSTACLES:
            dist = np.sqrt((x - obstacle["x"])**2 + (y - obstacle["y"])**2)
            min_obstacle_dist = min(min_obstacle_dist, dist)
        features.append(min_obstacle_dist)
        
        # Distance to nearest furniture
        min_furniture_dist = 999
        if placed_items:
            for item in placed_items:
                dist = np.sqrt((x - item["x"])**2 + (y - item["y"])**2)
                min_furniture_dist = min(min_furniture_dist, dist)
        features.append(min_furniture_dist)
        
        # Number of nearby furniture (within 2m radius)
        nearby_count = sum(1 for item in placed_items 
                          if np.sqrt((x - item["x"])**2 + (y - item["y"])**2) < 2.0)
        features.append(nearby_count)
        
        # Furniture type encoding (one-hot style)
        furniture_types = list(AILayoutTrainer.FURNITURE_CATALOG.keys())
        type_index = furniture_types.index(furniture_type) if furniture_type in furniture_types else -1
        features.append(type_index)
        
        # Zone encoding
        zone_mapping = {"living": 0, "dining": 1, "outdoor": 2, "decoration": 3}
        features.append(zone_mapping.get(zone_name, -1))
        
        return features
    
    @staticmethod
    def calculate_quality_score(x: float, y: float, panjang: float, lebar: float,
                               zone_name: str, placed_items: List[Dict]) -> float:
        """Calculate quality score for a position (0-1, higher is better)"""
        zone = AILayoutTrainer.ZONES.get(zone_name)
        score = 1.0
        
        # Prefer center of zone
        zone_center_x = (zone["x_min"] + zone["x_max"]) / 2
        zone_center_y = (zone["y_min"] + zone["y_max"]) / 2
        center_dist = np.sqrt((x - zone_center_x)**2 + (y - zone_center_y)**2)
        score *= (1.0 - min(center_dist / 10.0, 0.5))  # Max 50% penalty
        
        # Prefer positions away from obstacles
        min_obstacle_dist = 999
        for obstacle in AILayoutTrainer.OBSTACLES:
            dist = np.sqrt((x - obstacle["x"])**2 + (y - obstacle["y"])**2)
            min_obstacle_dist = min(min_obstacle_dist, dist)
        if min_obstacle_dist < 1.0:
            score *= 0.5  # Heavy penalty for being too close
        
        # Prefer even spacing from other furniture
        if placed_items:
            distances = [np.sqrt((x - item["x"])**2 + (y - item["y"])**2) 
                        for item in placed_items]
            avg_dist = np.mean(distances)
            if avg_dist < 1.0:
                score *= 0.7  # Penalty for clustering
        
        return max(score, 0.1)  # Minimum score 0.1
    
    @staticmethod
    def generate_training_data(num_samples: int = 5000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate training dataset with valid furniture placements"""
        X = []  # Features
        y_scores = []  # Target (quality scores)
        
        print(f"Generating {num_samples} training samples...")
        
        furniture_list = list(AILayoutTrainer.FURNITURE_CATALOG.items())
        samples_per_furniture = num_samples // len(furniture_list)
        
        for furniture_name, furniture_data in furniture_list:
            panjang = furniture_data["panjang"]
            lebar = furniture_data["lebar"]
            zone = furniture_data["zone"]
            
            print(f"  Processing {furniture_name} (zone: {zone})...")
            
            valid_samples = 0
            attempts = 0
            max_attempts = samples_per_furniture * 10
            
            while valid_samples < samples_per_furniture and attempts < max_attempts:
                attempts += 1
                
                # Random position in zone
                zone_data = AILayoutTrainer.ZONES[zone]
                pos_x = np.random.uniform(zone_data["x_min"], zone_data["x_max"] - panjang)
                pos_y = np.random.uniform(zone_data["y_min"], zone_data["y_max"] - lebar)
                
                # Simulate some placed items (0-5 random items)
                num_placed = np.random.randint(0, 6)
                placed_items = []
                for _ in range(num_placed):
                    placed_items.append({
                        "x": np.random.uniform(1, 15),
                        "y": np.random.uniform(1, 9),
                        "panjang": np.random.uniform(0.5, 2.5),
                        "lebar": np.random.uniform(0.5, 1.5)
                    })
                
                # Check if valid
                if AILayoutTrainer.is_valid_position(pos_x, pos_y, panjang, lebar, zone, placed_items):
                    features = AILayoutTrainer.calculate_position_features(
                        pos_x, pos_y, panjang, lebar, zone, placed_items, furniture_name
                    )
                    quality = AILayoutTrainer.calculate_quality_score(
                        pos_x, pos_y, panjang, lebar, zone, placed_items
                    )
                    
                    X.append(features)
                    y_scores.append(quality)
                    valid_samples += 1
        
        print(f"Generated {len(X)} valid training samples")
        return np.array(X), np.array(y_scores)
    
    @staticmethod
    def train_model(X: np.ndarray, y: np.ndarray) -> Tuple[RandomForestRegressor, Dict]:
        """Train Random Forest model"""
        print("\nTraining Random Forest model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        train_mse = mean_squared_error(y_train, train_pred)
        test_mse = mean_squared_error(y_test, test_pred)
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        
        metrics = {
            "train_mse": float(train_mse),
            "test_mse": float(test_mse),
            "train_r2": float(train_r2),
            "test_r2": float(test_r2),
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        }
        
        print(f"\n=== Model Performance ===")
        print(f"Train MSE: {train_mse:.6f}")
        print(f"Test MSE: {test_mse:.6f}")
        print(f"Train R²: {train_r2:.4f}")
        print(f"Test R²: {test_r2:.4f}")
        print(f"Accuracy: {test_r2 * 100:.2f}%")
        
        return model, metrics
    
    @staticmethod
    def save_model(model: RandomForestRegressor, metrics: Dict, 
                   model_path: str = "furniture_layout_model.pkl",
                   metrics_path: str = "model_metrics.json"):
        """Save trained model and metrics"""
        print(f"\nSaving model to {model_path}...")
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Saving metrics to {metrics_path}...")
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print("Model saved successfully!")
    
    @staticmethod
    def train_and_save():
        """Complete training pipeline"""
        print("=== AI Layout Trainer ===")
        print("Training Random Forest model for furniture placement\n")
        
        # Generate data
        X, y = AILayoutTrainer.generate_training_data(num_samples=5000)
        
        # Train model
        model, metrics = AILayoutTrainer.train_model(X, y)
        
        # Save model
        AILayoutTrainer.save_model(model, metrics)
        
        print("\n✅ Training complete!")
        return model, metrics


if __name__ == "__main__":
    # Run training
    model, metrics = AILayoutTrainer.train_and_save()
