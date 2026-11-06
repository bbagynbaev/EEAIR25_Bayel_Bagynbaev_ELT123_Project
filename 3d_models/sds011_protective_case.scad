box_width = 90;
box_length = 120;
box_height = 45;
wall_thickness = 2;

$fn = 60;

module enclosure() {
    difference() {
        cube([box_width, box_length, box_height]);
        
        translate([wall_thickness, wall_thickness, wall_thickness])
            cube([box_width - 2*wall_thickness, box_length - 2*wall_thickness, box_height]);
            
        translate([box_width/2, 0, box_height/2])
            rotate([90, 0, 0])
            cylinder(h=wall_thickness*4, r=4.5, center=true);
            
        translate([box_width/2, box_length, 12])
            cube([12, wall_thickness*4, 8], center=true);
            
        for (i = [20 : 10 : box_width-20]) {
            translate([i, box_length, 25])
                cube([3, wall_thickness*4, 15], center=true);
        }
    }
    
    standoff(10, 10);
    standoff(80, 10);
    standoff(10, 110);
    standoff(80, 110);
}

module standoff(x, y) {
    translate([x, y, wall_thickness])
        difference() {
            cylinder(h=5, r=3.5); 
            cylinder(h=6, r=1.5); 
        }
}

module lid() {
    cube([box_width, box_length, wall_thickness]);
    
    translate([wall_thickness + 0.2, wall_thickness + 0.2, wall_thickness])
        cube([box_width - 2*(wall_thickness + 0.2), box_length - 2*(wall_thickness + 0.2), 2]);
}

color("SteelBlue") enclosure();

translate([box_width + 10, 0, 0])
    color("LightGray") lid();