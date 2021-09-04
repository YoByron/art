// These are interesting settings. Vary ZOOM from 1 to how high you want.
// private static final int ZOOM = 12;
// private static final double COMPLEX_WIDTH = Math.pow(10, -ZOOM);
// private static final double CENTER_REAL = -0.743643887037151;
// private static final double CENTER_IMAGINARY = 0.131825904205330;
// private static final int MAX_ITERATIONS = 100 + 400 * (ZOOM - 1);

import processing.core.PApplet;

public class Mandelbrot extends PApplet {

    private static final double COMPLEX_WIDTH = 3.5;
    private static final double CENTER_REAL = -0.5;
    private static final double CENTER_IMAGINARY = 0;
    private static final int MAX_ITERATIONS = 128;
    private static final int THRESHOLD = 2;

    private static int defaultWidth = 1200;
    private static int defaultHeight = 800;

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
    }

    @Override
    public void draw() {
        loadPixels();

        final double[] reals = calculateReals();
        final double[] imaginaries = calculateImaginaries();

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
                    // Square the threshold to get rid of the expensive square root.
                    final int thresholdSquared = THRESHOLD * THRESHOLD;
                    while (n < MAX_ITERATIONS && abs < thresholdSquared) {
                        imSquared = im * im;
                        im = 2 * re * im + cImaginary;  // must come before the next line because it modifies re
                        final double reSquared = re * re;
                        re = reSquared - imSquared + cReal;
                        abs = reSquared + imSquared;
                        n++;
                    }
                }

                if (n >= MAX_ITERATIONS) {
                    pixels[x + y * width] = color(0);
                } else {
                    pixels[x + y * width] = color(map(n, 0, MAX_ITERATIONS, 75, 255));
                }

            }
        }

        updatePixels();
    }

    double[] calculateReals() {
        final double realIncrement = COMPLEX_WIDTH / (width - 1);
        final double[] reals = new double[width];
        double real = CENTER_REAL - COMPLEX_WIDTH / 2;
        for (int i = 0; i < reals.length; i++) {
            reals[i] = real;
            real += realIncrement;
        }
        return reals;
    }

    double[] calculateImaginaries() {
        final double complexHeight = COMPLEX_WIDTH / width * height;
        final double imaginaryIncrement = complexHeight / (height - 1);
        final double[] imaginaries = new double[height];
        double imaginary = CENTER_IMAGINARY - complexHeight / 2;
        for (int i = 0; i < imaginaries.length; i++) {
            imaginaries[i] = imaginary;
            imaginary += imaginaryIncrement;
        }
        return imaginaries;
    }

}
