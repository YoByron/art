// Inspired by the video by The Coding Train on Youtube with the title
// What is the secret behind the curve algorithm invented by a French auto engineer? CC 163: Bézier
// https://www.youtube.com/watch?v=enNfb6p3j_g


PVector start;
PVector end;
PVector controlMouse = new PVector(0, 0);
PVector controlFixed;
int offset = 10;
int n_steps = 30;
float[] t = new float[n_steps + 1];


void setup() {
    size(1200, 800);
    noCursor();
    noFill();
    start = new PVector(offset, offset);
    end = new PVector(width - offset, height - offset);
    controlFixed = new PVector(width * 2 / 3, offset);
    float n = (float)n_steps;
    for (int i = 0; i <= n_steps; i++) {
        t[i] = i / n;
    }
}


void draw() {
    colorMode(RGB, 255);
    background(16, 16, 16);

    controlMouse.x = mouseX;
    controlMouse.y = mouseY;

    stroke(255);
    strokeWeight(5);
    point(start.x, start.y);
    point(controlMouse.x, controlMouse.y);
    point(controlFixed.x, controlFixed.y);
    point(end.x, end.y);

    strokeWeight(1);
    getQuadraticBezier(start, controlMouse, end, true, true);
    // getCubicBezier(start, controlMouse, controlFixed, end, true, true);
}


PVector[] getQuadraticBezier(PVector start, PVector controlMouse, PVector end,
        boolean drawNet, boolean rainbow) {
    PVector[] result = new PVector[t.length];
    if (rainbow) {
        colorMode(HSB, t.length);
    } else {
        colorMode(RGB, 255);
        stroke(255);
    }
    for (int i = 0; i < t.length; i++) {
        float t_ = t[i];
        PVector p1 = PVector.lerp(start, controlMouse, t_);
        PVector p2 = PVector.lerp(controlMouse, end, t_);
        result[i] = PVector.lerp(p1, p2, t_);
        if (drawNet) {
            if (rainbow) {
                stroke(i, t.length, t.length);
            }
            line(p1.x, p1.y, p2.x, p2.y);
        }
    }
    return result;
}


PVector[] getCubicBezier(PVector start, PVector control1, PVector control2, PVector end,
        boolean drawNet, boolean rainbow) {
    PVector[] first = getQuadraticBezier(start, control1, control2, false, false);
    PVector[] second = getQuadraticBezier(control1, control2, end, false, false);
    PVector[] result = new PVector[t.length];
    if (rainbow) {
        colorMode(HSB, t.length);
    } else {
        colorMode(RGB, 255);
        stroke(255);
    }
    for (int i = 0; i < t.length; i++) {
        float t_ = t[i];
        PVector p1 = first[i];
        PVector p2 = second[i];
        result[i] = PVector.lerp(p1, p2, t_);
        if (drawNet) {
            if (rainbow) {
                stroke(i, t.length, t.length);
            }
            line(p1.x, p1.y, p2.x, p2.y);
        }
    }
    return result;
}
