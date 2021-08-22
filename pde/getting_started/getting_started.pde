void setup() {
    size(800, 600);
    noCursor();
}

void draw() {
    if (mousePressed) {
        fill(0);
    } else {
        fill(255);
    }
    circle(mouseX, mouseY, 80);
}
