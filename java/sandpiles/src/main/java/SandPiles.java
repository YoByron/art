// https://en.wikipedia.org/wiki/Abelian_sandpile_model
// https://www.youtube.com/watch?v=1MtEUErz7Gg

// TODO: Make another sketch with 8 neighbors.
// TODO: Improve square_size = 1 by using the pixels array.

import processing.core.PApplet;

public class SandPiles extends PApplet {

    private static int defaultWidth = 800;
    private static int defaultHeight = 800;

    private static final boolean ANIMATE = true;
    private static final boolean ANIMATE_FAST = true;
    private static final int N_SAND = 250_000;
    private static final int SQUARE_SIZE = 2;
    private static final int SQUARE_SIZE_TWICE = SQUARE_SIZE * 2;
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
        background(colors[0]);
        if (!ANIMATE) {
            noLoop();
        }
        noStroke();
        pileWidth = width / SQUARE_SIZE_TWICE;
        pileHeight = height / SQUARE_SIZE_TWICE;
        pile = new int[pileWidth * pileHeight];
        nextPile = pile.clone();
        pile[pile.length - 1] = N_SAND;
    }

    @Override
    public void draw() {
        if (ANIMATE) {
            topple();
            if (ANIMATE_FAST) {
                for (int i = 0; i < 20; i++) {
                    topple();
                }
            }
        } else {
            boolean notFinished = true;
            while (notFinished) {
                notFinished = topple();
            }
        }

        for (int x = 0; x < pileWidth; x++) {
            for (int y = 0; y < pileHeight; y++) {
                final int n = pile[x + y * pileWidth];
                fill(n < 4 ? colors[n] : color(255));
                final int squareX = x * SQUARE_SIZE;
                final int squareY = y * SQUARE_SIZE;
                final int rightX = width - squareX - SQUARE_SIZE_TWICE;
                final int bottomY = height - squareY - SQUARE_SIZE_TWICE;
                // top left quadrant
                square(squareX, squareY, SQUARE_SIZE);
                // top right quadrant
                square(rightX, squareY, SQUARE_SIZE);
                // bottom left quadrant
                square(squareX, bottomY, SQUARE_SIZE);
                // bottom right quadrant
                square(rightX, bottomY, SQUARE_SIZE);
            }
        }
    }

    private boolean topple() {
        boolean notFinished = false;
        for (int x = 0; x < pileWidth; x++) {
            for (int y = 0; y < pileHeight; y++) {
                final int i = x + y * pileWidth;
                final int n = pile[i];
                if (n >= 4) {
                    notFinished = true;
                    final int nToDistribute = n / 4;
                    nextPile[i] = n % 4;

                    // left neighbor
                    if (x > 0) {
                        nextPile[i - 1] += nToDistribute;
                    }

                    // right neighbor
                    if (x < pileWidth - 1) {
                        if (x == pileWidth - 2) {
                            nextPile[i + 1] += nToDistribute + nToDistribute;
                        } else {
                            nextPile[i + 1] += nToDistribute;
                        }
                    }

                    // top neighbor
                    if (y > 0) {
                        nextPile[i - pileWidth] += nToDistribute;
                    }

                    // bottom neighbor
                    if (y < pileHeight - 1) {
                        if (y == pileHeight - 2) {
                            nextPile[i + pileWidth] += nToDistribute + nToDistribute;
                        } else {
                            nextPile[i + pileWidth] += nToDistribute;
                        }
                    }
                }
            }
        }
        System.arraycopy(nextPile, 0, pile, 0, pile.length);
        return notFinished;
    }
}
