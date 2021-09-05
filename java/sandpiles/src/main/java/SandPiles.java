// https://en.wikipedia.org/wiki/Abelian_sandpile_model
// https://www.youtube.com/watch?v=1MtEUErz7Gg

// This approach uses two arrays to store the current and the next state of the pile.
// Using only a single array is much faster but then the animation is no longer symmetric.
// TODO: Use symmetry to iterate over only a quarter of the pile. Then be clever with
//  the square coordinates so you don't have to copy the quarter to the other tree parts.

import processing.core.PApplet;

public class SandPiles extends PApplet {

    private static int defaultWidth = 800;
    private static int defaultHeight = 800;

    private static final boolean ANIMATE = true;
    private static final int N_SAND = 250_000;
    private final int[] colors = new int[] {
            color(10, 63, 255),
            color(128, 190, 255),
            color(255, 222, 0),
            color(123, 0, 0)
    };
    private int widthHalf;
    private int heightHalf;
    private int[] pile;
    private int[] nextPile;

    public static void main(final String[] args) {
        if (args.length == 2) {
            defaultWidth = Integer.parseInt(args[0]);
            defaultHeight = Integer.parseInt(args[1]);
        }
        PApplet.main(SandPiles.class.getName());
    }

    @Override
    public void settings() {
        size(defaultWidth, defaultHeight);
    }

    @Override
    public void setup() {
        if (!ANIMATE) {
            noLoop();
        }
        noStroke();
        widthHalf = width / 2;
        heightHalf = height / 2;
        pile = new int[widthHalf * heightHalf];
        nextPile = pile.clone();
        pile[pile.length / 2 - widthHalf / 2] = N_SAND;
    }

    @Override
    public void draw() {
        topple();

        for (int i = 0; i < pile.length; i++) {
            final int n = pile[i];
            fill(n < 4 ? colors[n] : color(255));
            final int x = i % widthHalf * 2;
            final int y = i / heightHalf * 2;
            square(x, y, 2);
        }
    }

    private void topple() {
        // final long startTime = System.nanoTime();
        boolean finished;
        do {
            finished = true;
            for (int i = 0; i < pile.length; i++) {
                final int n = pile[i];
                if (n >= 4) {
                    finished = false;
                    final int nToDistribute = n / 4;
                    nextPile[i] = n % 4;

                    // left neighbor
                    if (i > 0) {
                        nextPile[i - 1] += nToDistribute;
                    }

                    // right neighbor
                    if (i < pile.length - 1) {
                        nextPile[i + 1] += nToDistribute;
                    }

                    // top neighbor
                    if (i >= widthHalf) {
                        nextPile[i - widthHalf] += nToDistribute;
                    }

                    // bottom neighbor
                    if (i < pile.length - widthHalf) {
                        nextPile[i + widthHalf] += nToDistribute;
                    }
                }
            }
            System.arraycopy(nextPile, 0, pile, 0, pile.length);
        } while (!finished && !ANIMATE);
        // final long endTime = System.nanoTime();
        // System.out.println((endTime - startTime) / 1_000_000_000.0);
    }
}
