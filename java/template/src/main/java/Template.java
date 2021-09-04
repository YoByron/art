// Inspired by the video by The Coding Train on Youtube with the title
// What is the secret behind the curve algorithm invented by a French auto engineer? CC 163: Bézier
// https://www.youtube.com/watch?v=enNfb6p3j_g

import processing.core.PApplet;

public class Template extends PApplet {

    private static int defaultWidth = 1200;
    private static int defaultHeight = 800;

    public static void main(final String[] args) {
        if (args.length == 2) {
            defaultWidth = Integer.parseInt(args[0]);
            defaultHeight = Integer.parseInt(args[1]);
        }
        PApplet.main(Template.class.getName());
    }

    @Override
    public void settings() {
        // This method must be used for size(), smooth() and noSmooth().
        size(defaultWidth, defaultHeight);
    }

    @Override
    public void setup() {
    }

    @Override
    public void draw() {
    }

}
