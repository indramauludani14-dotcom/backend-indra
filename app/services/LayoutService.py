"""
Layout Service - Simple & Clean
Model .pkl sudah trained, backend cuma load & predict
"""
import joblib
import pandas as pd
import numpy as np
from config import Config


class LayoutService:
    """Service untuk furniture layout prediction menggunakan pre-trained model"""
    
    def __init__(self):
        """Load pre-trained model dari .pkl files"""
        try:
            # Load model components (pre-trained)
            self.model = joblib.load(Config.MODEL_PATH)
            self.feature_cols = joblib.load(Config.FEATURE_COLS_PATH)
            self.metadata = joblib.load(Config.METADATA_PATH)
            self.placed = []  # Track placed furniture
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            self.model = None
            self.feature_cols = None
            self.metadata = {}
            self.placed = []
    
    def predict_batch(self, items, room_type="living_room", floor_data=None):
        """
        Main prediction function - simple & clean
        Model .pkl sudah contain logic, kita cuma extract features & predict
        """
        self.placed = []  # Reset
        
        # Get room boundaries
        rooms = self._get_rooms(floor_data)
        obstacles = self._get_obstacles(floor_data)
        
        results = []
        for idx, item in enumerate(items):
            # Extract item data
            furn_id = item.get("id", idx)
            name = item.get("name", "Furniture")
            panjang = float(item.get("panjang", 100))
            lebar = float(item.get("lebar", 100))
            
            # STEP 1: Model prediction (model .pkl do the work!)
            x, y = self._predict(panjang, lebar, idx, rooms)
            
            # STEP 2: Ensure within bounds
            x, y = self._clamp_to_room(x, y, panjang, lebar, rooms)
            
            # STEP 3: Avoid obstacles (check BEFORE and AFTER)
            x, y = self._avoid_obstacles(x, y, panjang, lebar, obstacles)
            x, y = self._clamp_to_room(x, y, panjang, lebar, rooms)
            # Double-check obstacle clearance
            x, y = self._avoid_obstacles(x, y, panjang, lebar, obstacles)
            x, y = self._clamp_to_room(x, y, panjang, lebar, rooms)
            
            # STEP 4: Avoid collision with other furniture
            x, y = self._avoid_collision(x, y, panjang, lebar)
            x, y = self._clamp_to_room(x, y, panjang, lebar, rooms)
            
            # FINAL: Re-check obstacles one more time (CRITICAL!)
            x, y = self._final_obstacle_check(x, y, panjang, lebar, obstacles, rooms)
            
            # Build result
            results.append({
                "id": furn_id,
                "nama": name,
                "category": item.get("category", ""),
                "posisi_x": int(x),
                "posisi_y": int(y),
                "panjang": int(panjang),
                "lebar": int(lebar),
                "zone": self._get_zone(x, y, panjang, lebar),
                "rotation": 0
            })
            
            # Track placed
            self.placed.append({"x": x, "y": y, "w": panjang, "h": lebar})
        
        return results
    
    # ========== CORE FUNCTIONS (SIMPLE!) ==========
    
    def _predict(self, panjang, lebar, index, rooms):
        """Use ML model to predict position"""
        if self.model and self.feature_cols:
            try:
                # Extract features (9 dimensions)
                features = pd.DataFrame([[
                    panjang, lebar,
                    panjang * lebar,                      # area
                    panjang / lebar if lebar > 0 else 1,  # aspect_ratio
                    2 * (panjang + lebar),                # perimeter
                    np.sqrt(panjang**2 + lebar**2),       # diagonal
                    np.log1p(panjang * lebar),            # log_area
                    np.log1p(panjang),                    # log_panjang
                    np.log1p(lebar)                       # log_lebar
                ]], columns=self.feature_cols)
                
                # Predict using model .pkl
                pred = self.model.predict(features)[0]
                return float(pred[0]), float(pred[1])
            except:
                pass
        
        # Fallback: grid layout
        return self._grid_position(panjang, lebar, index, rooms)
    
    def _grid_position(self, panjang, lebar, index, rooms):
        """Simple grid fallback if model fails"""
        if rooms:
            # Use first/largest room
            room = max(rooms, key=lambda r: r.get("width", 0) * r.get("height", 0))
            rx, ry, rw, rh = room["x"], room["y"], room["width"], room["height"]
            
            # Grid layout
            cols = max(1, int((rw - 40) / 120))
            col = index % cols
            row = index // cols
            
            x = rx + 20 + (col * 120)
            y = ry + 20 + (row * 100)
        else:
            # Default grid
            cols = 3
            x = 100 + (index % cols) * 150
            y = 100 + (index // cols) * 150
        
        return x, y
    
    def _clamp_to_room(self, x, y, w, h, rooms):
        """Force furniture within room boundaries"""
        if not rooms:
            return max(50, min(750-w, x)), max(50, min(750-h, y))
        
        # Find best room
        best = max(rooms, key=lambda r: r.get("width", 0) * r.get("height", 0))
        rx, ry, rw, rh = best["x"], best["y"], best["width"], best["height"]
        
        # Clamp with padding
        pad = 15
        x = max(rx+pad, min(rx+rw-w-pad, x))
        y = max(ry+pad, min(ry+rh-h-pad, y))
        
        return x, y
    
    def _avoid_obstacles(self, x, y, w, h, obstacles):
        """Move away from obstacles (tangga, dinding, kolom) - AGGRESSIVE MODE"""
        if not obstacles:
            return x, y
            
        max_attempts = 15  # More attempts
        safety_margin = 50  # Larger safety margin
        
        for attempt in range(max_attempts):
            has_collision = False
            
            for obs in obstacles:
                ox, oy, ow, oh = obs["x"], obs["y"], obs["width"], obs["height"]
                
                # Check overlap with LARGE safety margin
                if not (x + w + safety_margin < ox or 
                       ox + ow + safety_margin < x or 
                       y + h + safety_margin < oy or 
                       oy + oh + safety_margin < y):
                    
                    has_collision = True
                    
                    # Calculate distance from obstacle center
                    furniture_cx = x + w/2
                    furniture_cy = y + h/2
                    obstacle_cx = ox + ow/2
                    obstacle_cy = oy + oh/2
                    
                    dx = furniture_cx - obstacle_cx
                    dy = furniture_cy - obstacle_cy
                    
                    # AGGRESSIVE movement away
                    move_dist = 80 + (attempt * 10)  # Increase distance each attempt
                    
                    if abs(dx) > abs(dy):
                        # Move horizontal
                        x += move_dist if dx > 0 else -move_dist
                    else:
                        # Move vertical  
                        y += move_dist if dy > 0 else -move_dist
                    
                    break  # Re-check after movement
            
            if not has_collision:
                return x, y  # Safe position found
        
        # If still colliding after max attempts, try random safe position
        # Find safe area far from all obstacles
        if obstacles:
            safe_x = obstacles[0]["x"] - w - 100  # Far left
            safe_y = obstacles[0]["y"] - h - 100  # Far top
            return safe_x, safe_y
        
        return x, y
    
    def _avoid_collision(self, x, y, w, h):
        """Avoid other furniture (spiral search dengan padding lebih besar)"""
        padding = 25  # Increased from 20
        
        for attempt in range(50):  # More attempts
            collision = False
            
            for p in self.placed:
                if not (x + w + padding < p["x"] or 
                       p["x"] + p["w"] + padding < x or 
                       y + h + padding < p["y"] or 
                       p["y"] + p["h"] + padding < y):
                    collision = True
                    break
            
            if not collision:
                return x, y
            
            # Spiral search (larger radius)
            angle = attempt * 40
            radius = (attempt + 1) * 35  # Increased radius
            x += radius * np.cos(np.radians(angle))
            y += radius * np.sin(np.radians(angle))
        
        return x, y
    
    # ========== HELPERS ==========
    
    def _get_rooms(self, floor_data):
        """Extract rooms from floor data"""
        if not floor_data:
            return [{"x": 60, "y": 60, "width": 680, "height": 680}]
        return floor_data.get("rooms", [{"x": 60, "y": 60, "width": 680, "height": 680}])
    
    def _get_obstacles(self, floor_data):
        """Extract obstacles from floor data"""
        if not floor_data:
            return []
        return floor_data.get("obstacles", []) + floor_data.get("stairs", [])
    
    def _get_zone(self, x, y, w, h):
        """Determine zone (9-grid)"""
        cx, cy = x + w/2, y + h/2
        
        if cx < 266:
            zone_x = "left"
        elif cx > 533:
            zone_x = "right"
        else:
            zone_x = "center"
        
        if cy < 266:
            return f"top-{zone_x}" if zone_x != "center" else "top"
        elif cy > 533:
            return f"bottom-{zone_x}" if zone_x != "center" else "bottom"
        else:
            return zone_x
    
    def _final_obstacle_check(self, x, y, w, h, obstacles, rooms):
        """Final check: if still overlapping obstacle, find completely safe position"""
        if not obstacles:
            return x, y
        
        safety = 50
        
        # Check if current position overlaps any obstacle
        for obs in obstacles:
            ox, oy, ow, oh = obs["x"], obs["y"], obs["width"], obs["height"]
            
            if not (x + w + safety < ox or ox + ow + safety < x or 
                   y + h + safety < oy or oy + oh + safety < y):
                
                # Still overlapping! Find safe position in room corners
                if rooms:
                    room = rooms[0]
                    rx, ry, rw, rh = room["x"], room["y"], room["width"], room["height"]
                    
                    # Try corners: top-left, top-right, bottom-left, bottom-right
                    candidates = [
                        (rx + 20, ry + 20),                          # Top-left
                        (rx + rw - w - 20, ry + 20),                 # Top-right
                        (rx + 20, ry + rh - h - 20),                 # Bottom-left
                        (rx + rw - w - 20, ry + rh - h - 20),        # Bottom-right
                    ]
                    
                    # Find first corner without obstacle
                    for cx, cy in candidates:
                        safe = True
                        for obs2 in obstacles:
                            ox2, oy2, ow2, oh2 = obs2["x"], obs2["y"], obs2["width"], obs2["height"]
                            if not (cx + w + safety < ox2 or ox2 + ow2 + safety < cx or 
                                   cy + h + safety < oy2 or oy2 + oh2 + safety < cy):
                                safe = False
                                break
                        
                        if safe:
                            return cx, cy
        
        return x, y
