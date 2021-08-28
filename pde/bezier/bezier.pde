PVector p1;
PVector p3;
PVector p4;

void setup() {
    size(800, 600);
    int offset = 10;
    p1 = new PVector(offset, height / 2);
    p3 = new PVector(width / 3, height - offset);
    p4 = new PVector(width - offset, height / 2);
    noCursor();
}

void draw() {
    PVector p2 = new PVector(mouseX, mouseY);
    background(152, 190, 100);
    strokeWeight(5);
    point(p1.x, p1.y);
    point(p2.x, p2.y);
    point(p3.x, p3.y);
    point(p4.x, p4.y);
    strokeWeight(1);
    noFill();
    bezier(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y);
}
