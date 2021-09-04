import processing.core.PApplet;

public class SandPiles extends PApplet {

    private static int defaultWidth = 800;
    private static int defaultHeight = 800;

    private static final int N_SAND = 10_000;
    private final int[] colors = new int[] {
            color(255, 255, 255),
            color(255, 255, 0),
            color(255, 165, 0),
            color(255, 0, 0)
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
        background(255);
    }

    @Override
    public void draw() {
        loadPixels();
        final int[] pile = new int[pixels.length];
        pile[pile.length / 2 - width / 2] = N_SAND;

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
                    final int topIndex = i - width;
                    if (topIndex >= 0) {
                        pile[topIndex] += nForNeighbor;
                    }

                    // bottom neighbor
                    final int bottomIndex = i + width;
                    if (bottomIndex < pile.length - 1) {
                        pile[bottomIndex] += nForNeighbor;
                    }
                }
            }
        }

        for (int i = 0; i < pixels.length; i++) {
            pixels[i] = color(colors[pile[i]]);
        }
        updatePixels();
    }

}
