"""
Simple Auto Layout Service - Deterministic Algorithm
No ML dependencies, guaranteed collision-free placement
"""

from typing import Dict, List, Optional
import random


class SimpleLayoutService:
    """Simple deterministic layout without ML"""
    
    ROOM_WIDTH = 17.0
    ROOM_HEIGHT = 11.0
    
    ZONES = {
        "living": {"x_min": 1.0, "x_max": 7.0, "y_min": 1.0, "y_max": 5.0},      # Living room
        "dining": {"x_min": 9.5, "x_max": 15.0, "y_min": 1.0, "y_max": 5.0},     # Dining area
        "outdoor": {"x_min": 2.0, "x_max": 15.0, "y_min": 7.2, "y_max": 9.0},    # Outdoor terrace
        "decoration": {"x_min": 2.5, "x_max": 15.0, "y_min": 2.0, "y_max": 9.0}  # Decoration (safer bounds)
    }
    
    OBSTACLES = [
        {"name": "Tangga Up L1", "x": 12.4, "y": 1.6, "width": 1.6, "height": 2.8},
        {"name": "Tangga Down L2", "x": 9.0, "y": 7.6, "width": 2.0, "height": 1.6},
        {"name": "Tangga Up L2", "x": 11.6, "y": 7.6, "width": 2.0, "height": 1.6},
        {"name": "Column 1", "x": 8.5, "y": 5.0, "width": 0.36, "height": 0.36},
        {"name": "Column 2", "x": 15.0, "y": 5.0, "width": 0.36, "height": 0.36},
        {"name": "Column 3", "x": 8.5, "y": 6.5, "width": 0.36, "height": 0.36},
        {"name": "Column 4", "x": 15.0, "y": 6.5, "width": 0.36, "height": 0.36}
    ]
    
    MIN_SPACING = 0.65  # 65cm spacing - SAFE & BALANCED!
    WALL_MARGIN = 0.45  # 45cm dari dinding
    OBSTACLE_MARGIN = 0.65  # 65cm dari tangga/kolom!
    
    FURNITURE_CATALOG = {
        # Living Room - Reduced for better spacing
        "SOFA 3 Seat": {"panjang": 2.6, "lebar": 1.0, "zone": "living", "quantity": 1, "priority": 1},
        "SOFA 1 Seat": {"panjang": 1.14, "lebar": 1.0, "zone": "living", "quantity": 2, "priority": 2},
        
        # Dining Room - More realistic quantities
        "Meja Makan": {"panjang": 2.4, "lebar": 1.0, "zone": "dining", "quantity": 1, "priority": 3},
        "Kursi Makan": {"panjang": 0.46, "lebar": 0.75, "zone": "dining", "quantity": 4, "priority": 8},
        "Lemari Piring": {"panjang": 1.2, "lebar": 0.6, "zone": "dining", "quantity": 1, "priority": 5},
        
        # Decoration - Art pieces
        "Lukisan Besar": {"panjang": 4.0, "lebar": 1.5, "zone": "decoration", "quantity": 1, "priority": 4},
        "Lukisan Kecil": {"panjang": 0.6, "lebar": 0.6, "zone": "decoration", "quantity": 2, "priority": 9},
        "Stand Lukisan": {"panjang": 0.6, "lebar": 0.75, "zone": "decoration", "quantity": 2, "priority": 10},
        "Rak Display": {"panjang": 2.0, "lebar": 0.5, "zone": "decoration", "quantity": 1, "priority": 7},
        
        # Outdoor - Terrace furniture
        "Meja Teras": {"panjang": 2.4, "lebar": 1.0, "zone": "outdoor", "quantity": 1, "priority": 6},
        "Kursi Teras": {"panjang": 0.46, "lebar": 0.75, "zone": "outdoor", "quantity": 2, "priority": 11},
        
        # Plants - Decorative
        "Pot Bunga Small": {"panjang": 0.36, "lebar": 0.36, "zone": "decoration", "quantity": 3, "priority": 12},
        "Pot Bunga Medium": {"panjang": 0.43, "lebar": 0.43, "zone": "decoration", "quantity": 2, "priority": 13},
        "Pot Bunga Large": {"panjang": 0.6, "lebar": 0.6, "zone": "decoration", "quantity": 2, "priority": 14},
        
        # Climate Control
        "Standing AC": {"panjang": 0.5, "lebar": 0.4, "zone": "living", "quantity": 1, "priority": 15}
    }
    
    @staticmethod
    def check_collision(x1, y1, w1, h1, x2, y2, w2, h2, spacing=0.5):
        """AABB collision with spacing"""
        return not (x1 + w1 + spacing <= x2 or 
                   x2 + w2 + spacing <= x1 or 
                   y1 + h1 + spacing <= y2 or 
                   y2 + h2 + spacing <= y1)
    
    @staticmethod
    def is_valid_position(x, y, panjang, lebar, zone_name, placed_items):
        """Check if position valid (all checks)"""
        zone = SimpleLayoutService.ZONES.get(zone_name)
        if not zone:
            return False
        
        margin = SimpleLayoutService.WALL_MARGIN
        
        # Zone bounds
        if not (x >= zone["x_min"] + margin and
                x + panjang <= zone["x_max"] - margin and
                y >= zone["y_min"] + margin and
                y + lebar <= zone["y_max"] - margin):
            return False
        
        # Obstacles
        for obs in SimpleLayoutService.OBSTACLES:
            if SimpleLayoutService.check_collision(
                x, y, panjang, lebar,
                obs["x"], obs["y"], obs["width"], obs["height"],
                spacing=SimpleLayoutService.OBSTACLE_MARGIN
            ):
                return False
        
        # Placed furniture
        for item in placed_items:
            if SimpleLayoutService.check_collision(
                x, y, panjang, lebar,
                item["x"], item["y"], item["panjang"], item["lebar"],
                spacing=SimpleLayoutService.MIN_SPACING
            ):
                return False
        
        return True
    
    @staticmethod
    def find_best_position(furniture_name, furniture_data, placed_items):
        """Find position with strategic placement"""
        zone = furniture_data["zone"]
        panjang = furniture_data["panjang"]
        lebar = furniture_data["lebar"]
        priority = furniture_data["priority"]
        
        zone_data = SimpleLayoutService.ZONES[zone]
        
        # Calculate zone dimensions
        zone_width = zone_data["x_max"] - zone_data["x_min"]
        zone_height = zone_data["y_max"] - zone_data["y_min"]
        
        # Strategy: Place high-priority items first in good positions
        positions = []
        
        # Grid size based on furniture size (larger grid for efficiency)
        grid_size = max(0.3, min(panjang, lebar) / 2)  # 30cm minimum or half furniture size
        
        margin = SimpleLayoutService.WALL_MARGIN
        spacing = SimpleLayoutService.MIN_SPACING
        
        # For large items (priority 1-5), try strategic positions first
        if priority <= 5:
            strategic_positions = [
                # Center of zone
                (zone_data["x_min"] + (zone_width - panjang) / 2, 
                 zone_data["y_min"] + (zone_height - lebar) / 2),
                # Top-left corner
                (zone_data["x_min"] + margin, zone_data["y_min"] + margin),
                # Top-right corner
                (zone_data["x_max"] - panjang - margin, zone_data["y_min"] + margin),
                # Bottom-left corner
                (zone_data["x_min"] + margin, zone_data["y_max"] - lebar - margin),
                # Bottom-right corner
                (zone_data["x_max"] - panjang - margin, zone_data["y_max"] - lebar - margin),
                # Along walls
                (zone_data["x_min"] + margin, zone_data["y_min"] + zone_height / 2 - lebar / 2),
                (zone_data["x_max"] - panjang - margin, zone_data["y_min"] + zone_height / 2 - lebar / 2),
            ]
            
            for x, y in strategic_positions:
                if (x >= zone_data["x_min"] + margin and 
                    x + panjang <= zone_data["x_max"] - margin and
                    y >= zone_data["y_min"] + margin and 
                    y + lebar <= zone_data["y_max"] - margin):
                    if SimpleLayoutService.is_valid_position(x, y, panjang, lebar, zone, placed_items):
                        return round(x, 2), round(y, 2)
        
        # Systematic grid search (reduced grid for performance)
        x = zone_data["x_min"] + margin
        while x <= zone_data["x_max"] - panjang - margin:
            y = zone_data["y_min"] + margin
            while y <= zone_data["y_max"] - lebar - margin:
                if SimpleLayoutService.is_valid_position(x, y, panjang, lebar, zone, placed_items):
                    positions.append((round(x, 2), round(y, 2)))
                    
                    # Early return for small items to save time
                    if priority > 10 and positions:
                        return positions[0]
                        
                y += grid_size
            x += grid_size
        
        if not positions:
            return None
        
        # Return first valid position
        return positions[0]
    
    @staticmethod
    def get_zone_color(zone):
        colors = {
            "living": "#4A90E2",
            "dining": "#E27D60",
            "outdoor": "#85C88A",
            "decoration": "#F4A259"
        }
        return colors.get(zone, "#95A5A6")
    
    @staticmethod
    def auto_place_all_furniture(room_width=17.0, room_height=11.0):
        """Place all furniture deterministically"""
        placed_items = []
        failed_items = []
        
        sorted_furniture = sorted(
            SimpleLayoutService.FURNITURE_CATALOG.items(),
            key=lambda x: x[1]["priority"]
        )
        
        total_items = sum(f[1]["quantity"] for f in sorted_furniture)
        placed_count = 0
        
        print(f"\n🎯 Starting Simple Auto Layout for {total_items} items...")
        
        for furniture_name, furniture_data in sorted_furniture:
            quantity = furniture_data["quantity"]
            
            for i in range(quantity):
                position = SimpleLayoutService.find_best_position(
                    furniture_name, furniture_data, placed_items
                )
                
                if position:
                    x, y = position
                    placed_item = {
                        "nama": furniture_name,
                        "x": x,
                        "y": y,
                        "panjang": furniture_data["panjang"],
                        "lebar": furniture_data["lebar"],
                        "zone": furniture_data["zone"],
                        "color": SimpleLayoutService.get_zone_color(furniture_data["zone"]),
                        "uid": f"{furniture_name}-{i}-{placed_count}"
                    }
                    placed_items.append(placed_item)
                    placed_count += 1
                    print(f"  ✓ Placed {furniture_name} ({placed_count}/{total_items})")
                else:
                    failed_items.append(furniture_name)
                    print(f"  ✗ Failed {furniture_name}")
        
        success_rate = (placed_count / total_items * 100) if total_items > 0 else 0
        
        print(f"\n{'='*50}")
        print(f"✅ Complete!")
        print(f"   Placed: {placed_count}/{total_items}")
        print(f"   Success: {success_rate:.1f}%")
        print(f"{'='*50}\n")
        
        return {
            "success": True,
            "placed_items": placed_items,
            "failed_items": failed_items,
            "total_items": total_items,
            "placed_count": placed_count,
            "success_rate": round(success_rate, 2),
            "model_used": False,
            "algorithm": "Deterministic Grid Sampling"
        }


# Alias
AutoLayoutService = SimpleLayoutService
AILayoutService = SimpleLayoutService
