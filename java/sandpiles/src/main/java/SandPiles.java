// https://en.wikipedia.org/wiki/Abelian_sandpile_model
// https://www.youtube.com/watch?v=1MtEUErz7Gg

import processing.core.PApplet;

public class SandPiles extends PApplet {

    private static int defaultWidth = 800;
    private static int defaultHeight = 800;

    private static final int N_SAND = 250_000;
    private final int[] colors = new int[] {
            color(10, 63, 255),
            color(128, 190, 255),
            color(255, 222, 0),
            color(123, 0, 0)
    };

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
        noLoop();
        noStroke();
    }

    @Override
    public void draw() {
        final int widthHalf = width / 2;
        final int heightHalf = height / 2;
        final int[] pile = new int[widthHalf * heightHalf];
        pile[pile.length / 2 - widthHalf / 2] = N_SAND;

        boolean finished = false;
        while (!finished) {
            finished = true;
            for (int i = 0; i < pile.length; i++) {
                final int n = pile[i];
                if (n >= 4) {
                    finished = false;
                    final int nForNeighbor = n / 4;
                    pile[i] = n % 4;

                    // left neighbor
                    if (i > 0) {
                        pile[i - 1] += nForNeighbor;
                    }

                    // right neighbor
                    if (i < pile.length - 1) {
                        pile[i + 1] += nForNeighbor;
                    }

                    // top neighbor
                    final int topIndex = i - widthHalf;
                    if (topIndex >= 0) {
                        pile[topIndex] += nForNeighbor;
                    }

                    // bottom neighbor
                    final int bottomIndex = i + widthHalf;
                    if (bottomIndex < pile.length - 1) {
                        pile[bottomIndex] += nForNeighbor;
                    }
                }
            }
        }

        for (int i = 0; i < pile.length; i++) {
            final int x = i % widthHalf;
            final int y = i / heightHalf;
            fill(colors[pile[i]]);
            square(x + x, y + y, 2);
        }
    }
}
