"""
Auto Layout Service
Automatic furniture placement with collision detection and optimization
"""
import numpy as np
from typing import List, Dict, Tuple
import json

class AutoLayoutService:
    """Service for automatic furniture placement with optimal positioning"""
    
    # LAYOUT CONSTRAINTS - LIMITED FURNITURE
    MAX_FURNITURE_ITEMS = 5  # Maximum 4-5 furniture pieces per layout
    MAX_FURNITURE_SIZE = 7.5  # Maximum size (panjang or lebar) 7.5 meters (750cm = 750px on 800px canvas)
    MIN_FURNITURE_SIZE = 0.3  # Minimum size 30cm
    MAX_TOTAL_AREA_RATIO = 0.30  # Max 30% of floor area can be occupied
    
    # Furniture database - LIMITED & SIZED: MAX 4-5 ITEMS
    FURNITURE_CATALOG = {
        "SOFA 3 Seat": {"panjang": 2.6, "lebar": 1.0, "quantity": 1, "zone": "living", "priority": 1},
        "SOFA 1 Seat Besar": {"panjang": 1.15, "lebar": 1.0, "quantity": 1, "zone": "living", "priority": 2},
        "Meja Lingkaran Kecil": {"panjang": 0.5, "lebar": 0.5, "quantity": 1, "zone": "living", "priority": 5},
        "Meja Makan": {"panjang": 2.4, "lebar": 1.0, "quantity": 1, "zone": "dining", "priority": 1},
        "Kursi Makan": {"panjang": 0.46, "lebar": 0.75, "quantity": 1, "zone": "dining", "priority": 2},
    }
    
    # Layout zones definition dengan obstacle avoidance (koordinat dalam meter)
    ZONES = {
        "living": {
            "x_min": 1.0, "x_max": 7.5, "y_min": 1.0, "y_max": 5.5,
            "obstacles": []  # Add stairs/columns if needed
        },
        "dining": {
            "x_min": 9.0, "x_max": 15.5, "y_min": 1.0, "y_max": 5.5,
            "obstacles": []  # Add stairs/columns if needed
        },
        "outdoor": {
            "x_min": 1.5, "x_max": 15.5, "y_min": 7.0, "y_max": 9.5,
            "obstacles": []
        },
        "decoration": {
            "x_min": 1.0, "x_max": 16.0, "y_min": 1.0, "y_max": 10.0,
            "obstacles": []
        }
    }
    
    # Obstacle definitions (stairs, columns, walls) - koordinat dalam meter
    OBSTACLES = [
        # Tangga Lantai 1
        {"name": "Tangga Up L1", "x": 12.4, "y": 1.6, "width": 1.6, "height": 2.8},
        # Tangga Lantai 2
        {"name": "Tangga Down L2", "x": 9.0, "y": 7.6, "width": 2.0, "height": 1.6},
        {"name": "Tangga Up L2", "x": 11.6, "y": 7.6, "width": 2.0, "height": 1.6},
        # Kolom struktural
        {"name": "Column 1", "x": 3.2, "y": 3.6, "width": 0.36, "height": 0.36},
        {"name": "Column 2", "x": 11.6, "y": 3.6, "width": 0.36, "height": 0.36},
        {"name": "Column 3", "x": 3.2, "y": 7.6, "width": 0.36, "height": 0.36},
        {"name": "Column 4", "x": 11.6, "y": 7.6, "width": 0.36, "height": 0.36}
    ]
    
    # Minimum spacing between furniture (dalam meter) - Optimized untuk 99% success
    MIN_SPACING = 0.6  # 60cm spacing (compact but safe)
    WALL_MARGIN = 0.3  # 30cm from walls
    OBSTACLE_MARGIN = 0.6  # 60cm from obstacles
    
    @staticmethod
    def check_collision(x1: float, y1: float, w1: float, h1: float,
                       x2: float, y2: float, w2: float, h2: float,
                       spacing: float = 0.6) -> bool:
        """
        Check if two furniture pieces collide with spacing buffer
        Uses adaptive spacing based on furniture size
        """
        # Adaptive spacing: much smaller for small items
        avg_size = ((w1 + h1 + w2 + h2) / 4)
        if avg_size < 0.6:  # Very small items (< 60cm avg)
            adaptive_spacing = spacing * 0.5
        elif avg_size < 1.2:  # Small-medium items
            adaptive_spacing = spacing * 0.6
        else:  # Large items
            adaptive_spacing = spacing
        
        # Expand bounding boxes by spacing/2 on all sides
        x1_min = x1 - adaptive_spacing / 2
        y1_min = y1 - adaptive_spacing / 2
        x1_max = x1 + w1 + adaptive_spacing / 2
        y1_max = y1 + h1 + adaptive_spacing / 2
        
        x2_min = x2 - adaptive_spacing / 2
        y2_min = y2 - adaptive_spacing / 2
        x2_max = x2 + w2 + adaptive_spacing / 2
        y2_max = y2 + h2 + adaptive_spacing / 2
        
        # Check overlap with expanded boxes
        overlap = not (x1_max <= x2_min or x2_max <= x1_min or 
                      y1_max <= y2_min or y2_max <= y1_min)
        
        return overlap
    
    @staticmethod
    def check_obstacle_collision(x: float, y: float, panjang: float, lebar: float) -> bool:
        """Check if furniture collides with any obstacle (stairs, columns)"""
        for obstacle in AutoLayoutService.OBSTACLES:
            # Check collision with obstacle including margin
            if AutoLayoutService.check_collision(
                x, y, panjang, lebar,
                obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"],
                spacing=AutoLayoutService.OBSTACLE_MARGIN
            ):
                return True
        return False
    
    @staticmethod
    def is_within_zone(x: float, y: float, panjang: float, lebar: float, 
                       zone_name: str) -> bool:
        """Check if furniture fits within its designated zone"""
        zone = AutoLayoutService.ZONES.get(zone_name)
        if not zone:
            return False
        
        # Check zone boundaries with wall margin
        margin = AutoLayoutService.WALL_MARGIN
        return (x >= zone["x_min"] + margin and 
                x + panjang <= zone["x_max"] - margin and
                y >= zone["y_min"] + margin and 
                y + lebar <= zone["y_max"] - margin)
    
    @staticmethod
    def calculate_grid_positions(zone_name: str, grid_size: float = 0.3) -> List[Tuple[float, float]]:
        """
        Generate grid positions within a zone
        Fine grid for maximum placement options
        """
        zone = AutoLayoutService.ZONES.get(zone_name)
        if not zone:
            return []
        
        positions = []
        margin = AutoLayoutService.WALL_MARGIN
        
        x = zone["x_min"] + margin
        while x < zone["x_max"] - margin:
            y = zone["y_min"] + margin
            while y < zone["y_max"] - margin:
                positions.append((round(x, 2), round(y, 2)))
                y += grid_size
            x += grid_size
        
        return positions
    
    @staticmethod
    def place_furniture_optimized(furniture_name: str, furniture_data: Dict,
                                  placed_items: List[Dict], 
                                  room_width: float = 17.0,
                                  room_height: float = 11.0) -> Dict:
        """
        Place furniture at optimal position with collision avoidance
        Uses intelligent positioning based on furniture type and zone
        """
        zone = furniture_data["zone"]
        panjang = furniture_data["panjang"]
        lebar = furniture_data["lebar"]
        
        # Get potential positions in priority order - FINE GRID for 99% success
        if zone == "wall":
            # Wall items go along the top wall
            positions = [(x, 0.5) for x in np.arange(1.0, room_width - panjang - 1.0, 0.3)]
        elif zone == "living":
            # Living room: center and symmetrical arrangement
            positions = AutoLayoutService.calculate_grid_positions(zone, grid_size=0.3)
            # Prioritize center positions
            center_x = (AutoLayoutService.ZONES[zone]["x_min"] + 
                       AutoLayoutService.ZONES[zone]["x_max"]) / 2
            center_y = (AutoLayoutService.ZONES[zone]["y_min"] + 
                       AutoLayoutService.ZONES[zone]["y_max"]) / 2
            positions.sort(key=lambda p: abs(p[0] - center_x) + abs(p[1] - center_y))
        elif zone == "dining":
            # Dining room: very dense grid for tables and chairs
            positions = AutoLayoutService.calculate_grid_positions(zone, grid_size=0.25)
            # Prioritize left side for tables, then spread chairs
            positions.sort(key=lambda p: p[0])
        elif zone == "outdoor":
            # Outdoor: moderate grid
            positions = AutoLayoutService.calculate_grid_positions(zone, grid_size=0.4)
        else:
            # Decoration: fine grid for filling empty spaces
            positions = AutoLayoutService.calculate_grid_positions(zone, grid_size=0.3)
        
        # Try each position
        for x, y in positions:
            # Check if within zone
            if not AutoLayoutService.is_within_zone(x, y, panjang, lebar, zone):
                continue
            
            # Check collision with obstacles (stairs, columns)
            if AutoLayoutService.check_obstacle_collision(x, y, panjang, lebar):
                continue
            
            # Check collision with all placed items
            collision = False
            for item in placed_items:
                if AutoLayoutService.check_collision(
                    x, y, panjang, lebar,
                    item["x"], item["y"], item["panjang"], item["lebar"],
                    spacing=AutoLayoutService.MIN_SPACING
                ):
                    collision = True
                    break
            
            if not collision:
                # Found valid position
                return {
                    "nama": furniture_name,
                    "x": round(x, 2),
                    "y": round(y, 2),
                    "panjang": panjang,
                    "lebar": lebar,
                    "zone": zone,
                    "color": AutoLayoutService.get_zone_color(zone)
                }
        
        # If no position found, return None
        return None
    
    @staticmethod
    def get_zone_color(zone: str) -> str:
        """Get color based on zone"""
        colors = {
            "living": "#4A90E2",
            "dining": "#E27D60",
            "outdoor": "#85C88A",
            "decoration": "#F4A259",
            "wall": "#9B59B6"
        }
        return colors.get(zone, "#95A5A6")
    
    @staticmethod
    def validate_no_overlap(placed_items: List[Dict]) -> Dict:
        """
        VALIDATION: Check if ANY furniture overlaps
        Returns detailed collision report
        """
        collisions = []
        warnings = []
        
        for i in range(len(placed_items)):
            for j in range(i + 1, len(placed_items)):
                item1 = placed_items[i]
                item2 = placed_items[j]
                
                # Check ACTUAL overlap (no spacing buffer)
                x1, y1, w1, h1 = item1["x"], item1["y"], item1["panjang"], item1["lebar"]
                x2, y2, w2, h2 = item2["x"], item2["y"], item2["panjang"], item2["lebar"]
                
                # AABB overlap test
                overlap = not (x1 + w1 <= x2 or x2 + w2 <= x1 or 
                              y1 + h1 <= y2 or y2 + h2 <= y1)
                
                if overlap:
                    collisions.append({
                        "item1": item1["nama"],
                        "item2": item2["nama"],
                        "pos1": f"({x1:.2f}, {y1:.2f})",
                        "pos2": f"({x2:.2f}, {y2:.2f})"
                    })
                else:
                    # Check if too close (within minimum spacing)
                    min_edge_dist = min(
                        abs(x1 + w1 - x2),
                        abs(x2 + w2 - x1),
                        abs(y1 + h1 - y2),
                        abs(y2 + h2 - y1)
                    )
                    
                    if min_edge_dist < AutoLayoutService.MIN_SPACING:
                        warnings.append({
                            "item1": item1["nama"],
                            "item2": item2["nama"],
                            "distance": f"{min_edge_dist:.2f}m"
                        })
        
        return {
            "overlap_count": len(collisions),
            "warning_count": len(warnings),
            "collisions": collisions,
            "warnings": warnings,
            "status": "CLEAN" if len(collisions) == 0 else "HAS_OVERLAP"
        }
    
    @staticmethod
    def validate_furniture_constraints(furniture_name: str, furniture_data: Dict, 
                                       placed_items: List[Dict],
                                       room_width: float, room_height: float) -> Dict:
        """
        Validate furniture against size and capacity constraints
        Returns: {valid: bool, reason: str}
        """
        panjang = furniture_data["panjang"]
        lebar = furniture_data["lebar"]
        
        # Check maximum items limit
        if len(placed_items) >= AutoLayoutService.MAX_FURNITURE_ITEMS:
            return {
                "valid": False, 
                "reason": f"Maximum {AutoLayoutService.MAX_FURNITURE_ITEMS} items limit reached"
            }
        
        # Check furniture size constraints
        if panjang > AutoLayoutService.MAX_FURNITURE_SIZE or lebar > AutoLayoutService.MAX_FURNITURE_SIZE:
            return {
                "valid": False,
                "reason": f"Furniture too large (max {AutoLayoutService.MAX_FURNITURE_SIZE}m per dimension)"
            }
        
        if panjang < AutoLayoutService.MIN_FURNITURE_SIZE or lebar < AutoLayoutService.MIN_FURNITURE_SIZE:
            return {
                "valid": False,
                "reason": f"Furniture too small (min {AutoLayoutService.MIN_FURNITURE_SIZE}m per dimension)"
            }
        
        # Check total area constraint
        room_area = room_width * room_height
        current_furniture_area = sum(item["panjang"] * item["lebar"] for item in placed_items)
        new_furniture_area = panjang * lebar
        total_area = current_furniture_area + new_furniture_area
        area_ratio = total_area / room_area
        
        if area_ratio > AutoLayoutService.MAX_TOTAL_AREA_RATIO:
            return {
                "valid": False,
                "reason": f"Floor capacity exceeded ({area_ratio*100:.1f}% > {AutoLayoutService.MAX_TOTAL_AREA_RATIO*100}% limit)"
            }
        
        return {"valid": True, "reason": "OK"}
    
    @staticmethod
    def auto_place_all_furniture(room_width: float = 17.0, 
                                room_height: float = 11.0) -> Dict:
        """
        Automatically place all furniture in the catalog
        LIMITED TO MAX 4-5 ITEMS with size and floor constraints
        Returns optimized layout with high accuracy and retry mechanism
        """
        placed_items = []
        failed_items = []
        
        # Sort furniture by priority (important items first)
        sorted_furniture = sorted(
            AutoLayoutService.FURNITURE_CATALOG.items(),
            key=lambda x: (x[1]["priority"], -x[1]["panjang"] * x[1]["lebar"])  # Priority, then by size
        )
        
        max_retries = 3
        retry_count = 0
        
        print("\n" + "="*60)
        print("🪑 AUTO LAYOUT - LIMITED FURNITURE MODE")
        print("="*60)
        print(f"Max Items: {AutoLayoutService.MAX_FURNITURE_ITEMS}")
        print(f"Max Size: {AutoLayoutService.MAX_FURNITURE_SIZE}m")
        print(f"Max Floor Coverage: {AutoLayoutService.MAX_TOTAL_AREA_RATIO*100}%")
        print("="*60)
        
        # Place each furniture type with constraints validation
        for furniture_name, furniture_data in sorted_furniture:
            quantity = furniture_data["quantity"]
            
            for i in range(quantity):
                # Validate furniture constraints before placement
                validation = AutoLayoutService.validate_furniture_constraints(
                    furniture_name, furniture_data, placed_items, room_width, room_height
                )
                
                if not validation["valid"]:
                    failed_items.append({
                        "nama": furniture_name,
                        "reason": validation["reason"]
                    })
                    print(f"❌ {furniture_name}: {validation['reason']}")
                    continue
                
                result = None
                attempts = 0
                max_attempts = 15  # Maximum attempts untuk 99% success
                
                # Try placing with increasing flexibility
                while result is None and attempts < max_attempts:
                    result = AutoLayoutService.place_furniture_optimized(
                        furniture_name,
                        furniture_data,
                        placed_items,
                        room_width,
                        room_height
                    )
                    attempts += 1
                    
                    # Progressive spacing relaxation (more aggressive)
                    if result is None and attempts > 2:
                        old_spacing = AutoLayoutService.MIN_SPACING
                        # Gradually reduce spacing more aggressively
                        reduction = min(0.4, 0.08 * (attempts - 2))
                        AutoLayoutService.MIN_SPACING = max(0.25, old_spacing - reduction)
                        
                        result = AutoLayoutService.place_furniture_optimized(
                            furniture_name,
                            furniture_data,
                            placed_items,
                            room_width,
                            room_height
                        )
                        AutoLayoutService.MIN_SPACING = old_spacing
                
                if result:
                    # Add unique ID
                    result["uid"] = len(placed_items) + 1
                    placed_items.append(result)
                    print(f"✅ {furniture_name} placed at ({result['x']:.2f}, {result['y']:.2f})")
                    
                    # Stop if max items reached
                    if len(placed_items) >= AutoLayoutService.MAX_FURNITURE_ITEMS:
                        print(f"⚠️ Maximum {AutoLayoutService.MAX_FURNITURE_ITEMS} items limit reached!")
                        break
                else:
                    failed_items.append({
                        "nama": furniture_name,
                        "reason": f"No valid position found after {max_attempts} attempts"
                    })
            
            # Break outer loop if max items reached
            if len(placed_items) >= AutoLayoutService.MAX_FURNITURE_ITEMS:
                break
        
        # Calculate statistics
        total_items = sum(f["quantity"] for f in AutoLayoutService.FURNITURE_CATALOG.values())
        total_items = min(total_items, AutoLayoutService.MAX_FURNITURE_ITEMS)  # Cap at max items
        success_rate = (len(placed_items) / total_items) * 100 if total_items > 0 else 0
        
        # Calculate floor coverage
        room_area = room_width * room_height
        furniture_area = sum(item["panjang"] * item["lebar"] for item in placed_items)
        coverage_ratio = (furniture_area / room_area) * 100
        
        # VALIDATION: Check for overlaps
        validation = AutoLayoutService.validate_no_overlap(placed_items)
        
        print("\n" + "="*60)
        print("📊 AUTO LAYOUT VALIDATION REPORT (LIMITED MODE)")
        print("="*60)
        print(f"Max Items Allowed: {AutoLayoutService.MAX_FURNITURE_ITEMS}")
        print(f"Items Placed: {len(placed_items)}/{AutoLayoutService.MAX_FURNITURE_ITEMS}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Floor Coverage: {coverage_ratio:.1f}% (Max: {AutoLayoutService.MAX_TOTAL_AREA_RATIO*100}%)")
        print(f"Overlap Status: {validation['status']}")
        print(f"  - Overlaps: {validation['overlap_count']}")
        print(f"  - Close Spacing Warnings: {validation['warning_count']}")
        
        if validation['collisions']:
            print("\n⚠️ COLLISIONS DETECTED:")
            for c in validation['collisions'][:5]:  # Show first 5
                print(f"  - {c['item1']} vs {c['item2']}")
        else:
            print("\n✅ NO OVERLAPS - Layout is CLEAN!")
        
        if failed_items:
            print(f"\n❌ FAILED TO PLACE ({len(failed_items)} items):")
            for f in failed_items[:5]:  # Show first 5
                print(f"  - {f['nama']}: {f['reason']}")
        
        print("="*60 + "\n")
        
        return {
            "status": "success",
            "placed_count": len(placed_items),
            "failed_count": len(failed_items),
            "total_items": total_items,
            "max_items": AutoLayoutService.MAX_FURNITURE_ITEMS,
            "success_rate": round(success_rate, 2),
            "floor_coverage": round(coverage_ratio, 2),
            "max_coverage": AutoLayoutService.MAX_TOTAL_AREA_RATIO * 100,
            "placed_items": placed_items,
            "failed_items": failed_items,
            "room_dimensions": {
                "width": room_width,
                "height": room_height
            },
            "validation": validation,
            "constraints": {
                "max_items": AutoLayoutService.MAX_FURNITURE_ITEMS,
                "max_size": AutoLayoutService.MAX_FURNITURE_SIZE,
                "max_coverage": AutoLayoutService.MAX_TOTAL_AREA_RATIO * 100
            }
        }
    
    @staticmethod
    def optimize_dining_chairs(placed_items: List[Dict], table_name: str = "Meja Makan") -> List[Dict]:
        """
        Optimize chair placement around dining tables
        Places chairs symmetrically around each table
        """
        optimized = []
        tables = [item for item in placed_items if table_name in item["nama"]]
        chairs = [item for item in placed_items if "Kursi Makan" in item["nama"]]
        other_items = [item for item in placed_items 
                      if table_name not in item["nama"] and "Kursi Makan" not in item["nama"]]
        
        chair_index = 0
        for table in tables:
            # Calculate positions around table
            table_x = table["x"]
            table_y = table["y"]
            table_w = table["panjang"]
            table_h = table["lebar"]
            
            chair_w = 0.46
            chair_h = 0.75
            spacing = 0.6
            
            # Place chairs: 3 on each long side, 1 on each short side (6 chairs per table)
            positions = [
                # Left side (3 chairs)
                (table_x - chair_w - spacing, table_y + 0.1),
                (table_x - chair_w - spacing, table_y + table_h/2 - chair_h/2),
                (table_x - chair_w - spacing, table_y + table_h - chair_h - 0.1),
                # Right side (3 chairs)
                (table_x + table_w + spacing, table_y + 0.1),
                (table_x + table_w + spacing, table_y + table_h/2 - chair_h/2),
                (table_x + table_w + spacing, table_y + table_h - chair_h - 0.1),
            ]
            
            for pos_x, pos_y in positions:
                if chair_index < len(chairs):
                    chair = chairs[chair_index].copy()
                    chair["x"] = round(pos_x, 2)
                    chair["y"] = round(pos_y, 2)
                    optimized.append(chair)
                    chair_index += 1
        
        return other_items + tables + optimized
