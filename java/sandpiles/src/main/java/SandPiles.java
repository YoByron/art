// https://en.wikipedia.org/wiki/Abelian_sandpile_model
// https://www.youtube.com/watch?v=1MtEUErz7Gg

// This approach uses two arrays to store the current and the next state of the pile.
// Using only a single array is much faster but then the animation is no longer symmetric.
// TODO: Use symmetry to iterate over only a quarter of the pile. Then be clever with
//  the square coordinates so you don't have to copy the quarter to the other tree parts.
// But that only works if I drop sand into that quarter. Someday I want to make it interactive,
// so that the user can drop some sand by clicking the mouse. But then speed won't be so important.

import processing.core.PApplet;

public class SandPiles extends PApplet {

    private static int defaultWidth = 800;
    private static int defaultHeight = 800;

    private static final boolean ANIMATE = false;
    private static final int N_SAND = 250_000;
    private final int[] colors = new int[] {
            color(10, 63, 255),
            color(128, 190, 255),
            color(255, 222, 0),
            color(123, 0, 0)
    };
    private int pileWidth;
    private int pileHeight;
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
        pileWidth = width / 2;
        pileHeight = height / 2;
        pile = new int[pileWidth * pileHeight];
        nextPile = pile.clone();
        pile[pile.length / 2 - pileWidth / 2] = N_SAND;
    }

    @Override
    public void draw() {

        if (ANIMATE) {
            topple();
        } else {
            final long startTime = System.nanoTime();
            boolean notFinished = true;
            while (notFinished) {
                notFinished = topple();
            }
            final long endTime = System.nanoTime();
            System.out.println((endTime - startTime) / 1_000_000_000.0);
        }

        for (int x = 0; x < pileWidth; x++) {
            for (int y = 0; y < pileHeight; y++) {
                final int n = pile[x + y * pileWidth];
                fill(n < 4 ? colors[n] : color(255));
                square(x + x, y + y, 2);
            }
        }
    }

    private boolean topple() {
        boolean notFinished = false;
        for (int i = 0; i < pile.length; i++) {
            final int n = pile[i];
            if (n >= 4) {
                notFinished = true;
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
                if (i >= pileWidth) {
                    nextPile[i - pileWidth] += nToDistribute;
                }

                // bottom neighbor
                if (i < pile.length - pileWidth) {
                    nextPile[i + pileWidth] += nToDistribute;
                }
            }
        }
        System.arraycopy(nextPile, 0, pile, 0, pile.length);
        return notFinished;
    }
}
