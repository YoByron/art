// Inspired by the video by The Coding Train on Youtube with the title
// What is the secret behind the curve algorithm invented by a French auto engineer? CC 163: Bézier
// https://www.youtube.com/watch?v=enNfb6p3j_g

import processing.core.PApplet;

public class Mandelbrot extends PApplet {

    private static int defaultWidth = 1200;
    private static int defaultHeight = 800;

    private static final double COMPLEX_WIDTH = 3.5;
    private static final double CENTER_REAL = -0.5;
    private static final double CENTER_IMAGINARY = 0;
    private static final int MAX_ITERATIONS = 128;
    // Usually THRESHOLD would be 2 but if I square it I can get rid of one expensive sqrt.
    private static final int THRESHOLD = 4;

    private double[] reals;
    private double[] imaginaries;

    public static void main(final String[] args) {
        if (args.length == 2) {
            defaultWidth = Integer.parseInt(args[0]);
            defaultHeight = Integer.parseInt(args[1]);
        }
        PApplet.main(Mandelbrot.class.getName());
    }

    @Override
    public void settings() {
        size(defaultWidth, defaultHeight);
    }

    @Override
    public void setup() {
        noLoop();

        final double complexHeight = COMPLEX_WIDTH / width * height;
        final double realMin = CENTER_REAL - COMPLEX_WIDTH / 2;
        final double imaginaryMin = CENTER_IMAGINARY - complexHeight / 2;
        final double realIncrement = COMPLEX_WIDTH / (width - 1);
        final double imaginaryIncrement = complexHeight / (height - 1);

        reals = new double[width];
        double real = realMin;
        for (int i = 0; i < reals.length; i++) {
            reals[i] = real;
            real += realIncrement;
        }

        imaginaries = new double[height];
        double imaginary = imaginaryMin;
        for (int i = 0; i < imaginaries.length; i++) {
            imaginaries[i] = imaginary;
            imaginary += imaginaryIncrement;
        }
    }

    @Override
    public void draw() {
        loadPixels();

        for (int x = 0; x < width; x++) {
            final double cReal = reals[x];
            for (int y = 0; y < height; y++) {
                final double cImaginary = imaginaries[y];

                double re = cReal;
                double im = cImaginary;

                // Check if the point is inside the cardioid or the period-2 bulb.
                double imSquared = im * im;
                final double re_ = re - 0.25;
                final double q = re_ * re_ + imSquared;
                final boolean insideCardioid = q * (q + re_) <= 0.25 * imSquared;
                final boolean insidePeriod2Bulb = (re + 1) * (re + 1) + imSquared <= 0.0625;

                int n = 0;
                if (insideCardioid || insidePeriod2Bulb) {
                    n = MAX_ITERATIONS;
                } else {
                    double abs = 0;
                    while (n < MAX_ITERATIONS && abs < THRESHOLD) {
                        imSquared = im * im;
                        im = 2 * re * im + cImaginary;  // must come before the next line because it modifies re
                        final double reSquared = re * re;
                        re = reSquared - imSquared + cReal;
                        abs = reSquared + imSquared;
                        n++;
                    }
                }

                if (n >= MAX_ITERATIONS) {
                    pixels[x+ y * width] = color(0);
                } else {
                    pixels[x + y * width] = color(map(n, 0, MAX_ITERATIONS, 75, 255));
                }

            }
        }

        updatePixels();
    }

}
