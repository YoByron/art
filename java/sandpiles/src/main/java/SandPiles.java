// https://en.wikipedia.org/wiki/Abelian_sandpile_model
// https://www.youtube.com/watch?v=1MtEUErz7Gg

// TODO: Variable square size. That one changes the pile size, too. And it means I have to calculate
//  stuff like twoX and twoY differently.

import processing.core.PApplet;

import java.util.Arrays;

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
        pileWidth = width / 4;
        pileHeight = height / 4;
        pile = new int[pileWidth * pileHeight];
        nextPile = pile.clone();
        pile[pile.length - 1] = N_SAND;
    }

    @Override
    public void draw() {
        if (ANIMATE) {
            topple();
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
                final int twoX = x + x;
                final int twoY = y + y;
                final int rightX = width - twoX - 2 * 2;
                final int bottomY = height - twoY - 2 * 2;
                // top left quadrant
                square(twoX, twoY, 2);

                // top right quadrant
                square(rightX, twoY, 2);

                // bottom left quadrant
                square(twoX, bottomY, 2);

                // bottom right quadrant
                square(rightX, bottomY, 2);
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
