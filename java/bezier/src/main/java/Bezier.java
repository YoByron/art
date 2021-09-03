// Inspired by the video by The Coding Train on Youtube with the title
// What is the secret behind the curve algorithm invented by a French auto engineer? CC 163: Bézier
// https://www.youtube.com/watch?v=enNfb6p3j_g

import processing.core.PApplet;
import processing.core.PVector;

public class Bezier extends PApplet {

    private static final int OFFSET = 10;
    private static final int N_STEPS = 30;
    private static final float[] T = new float[N_STEPS + 1];
    private static int widthArg;
    private static int heightArg;
    private PVector start;
    private PVector controlFixed;
    private PVector controlMouse;
    private PVector end;

    public static void main(final String[] args) {
        if (args.length == 2) {
            widthArg = Integer.parseInt(args[0]);
            heightArg = Integer.parseInt(args[1]);
        } else {
            widthArg = 1200;
            heightArg = 800;
        }
        PApplet.main("Bezier");
    }

    @Override
    public void settings() {
        size(widthArg, heightArg);
    }

    @Override
    public void setup() {
        noCursor();
        noFill();
        start = new PVector(OFFSET, OFFSET);
        controlFixed = new PVector(width * 2 / 3f, OFFSET);
        controlMouse = new PVector(mouseX, mouseY);
        end = new PVector(width - OFFSET, height - OFFSET);
        for (int i = 0; i <= N_STEPS; i++) {
            T[i] = (float) i / N_STEPS;
        }
    }

    @Override
    public void draw() {
        colorMode(RGB, 255);
        background(16, 16, 16);

        controlMouse.set(mouseX, mouseY);

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

    private PVector[] getQuadraticBezier(final PVector start, final PVector control, final PVector end,
                                         final boolean drawNet, final boolean rainbow) {
        final PVector[] result = new PVector[T.length];
        if (rainbow) {
            colorMode(HSB, T.length);
        } else {
            colorMode(RGB, 255);
            stroke(255);
        }
        for (int i = 0; i < T.length; i++) {
            final float t = T[i];
            final PVector p1 = PVector.lerp(start, control, t);
            final PVector p2 = PVector.lerp(control, end, t);
            result[i] = PVector.lerp(p1, p2, t);
            if (drawNet) {
                if (rainbow) {
                    stroke(i, T.length, T.length);
                }
                line(p1.x, p1.y, p2.x, p2.y);
            }
        }
        return result;
    }

    private PVector[] getCubicBezier(final PVector start, final PVector control1, final PVector control2,
                                     final PVector end, final boolean drawNet, final boolean rainbow) {
        final PVector[] first = getQuadraticBezier(start, control1, control2, false, false);
        final PVector[] second = getQuadraticBezier(control1, control2, end, false, false);
        final PVector[] result = new PVector[T.length];
        if (rainbow) {
            colorMode(HSB, T.length);
        } else {
            colorMode(RGB, 255);
            stroke(255);
        }
        for (int i = 0; i < T.length; i++) {
            final float t = T[i];
            final PVector p1 = first[i];
            final PVector p2 = second[i];
            result[i] = PVector.lerp(p1, p2, t);
            if (drawNet) {
                if (rainbow) {
                    stroke(i, T.length, T.length);
                }
                line(p1.x, p1.y, p2.x, p2.y);
            }
        }
        return result;
    }
}
