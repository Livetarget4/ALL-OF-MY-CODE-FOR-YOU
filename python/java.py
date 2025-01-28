import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class DotGame extends JPanel implements Runnable, KeyListener {
    private static final long serialVersionUID = 1L;

    private static final int SCREEN_WIDTH = 1600;
    private static final int SCREEN_HEIGHT = 850;
    private static final int DOT_SIZE = 10;
    private static final int OBSTACLE_SIZE = 15; // Increase obstacle size for better visibility
    private static final Color BG_COLOR = Color.WHITE;
    private static final Color DOT_COLOR = Color.BLUE;
    private static final Color OBSTACLE_COLOR = Color.RED;
    private static final Color SCORE_COLOR = Color.BLACK;
    private static final int FPS = 60;

    private int dotX = SCREEN_WIDTH / 2;
    private int dotY = SCREEN_HEIGHT / 2;
    private int dotSpeed = 4; // Movement speed of the dot

    // List to hold obstacle information
    private List<Obstacle> obstacles = new ArrayList<>();
    private int numObstacles = 66; // Number of obstacles

    // Initialize score
    private int score = 0;

    public DotGame() {
        // Create initial obstacles falling from the top
        Random rand = new Random();
        for (int i = 0; i < numObstacles; i++) {
            int obstacleX = rand.nextInt(SCREEN_WIDTH - OBSTACLE_SIZE);
            int obstacleY = rand.nextInt(-SCREEN_HEIGHT - OBSTACLE_SIZE); // Start above the visible screen
            int obstacleDx = 0; // No horizontal movement
            int obstacleDy = rand.nextInt(3) + 1; // Random initial downward velocity
            obstacles.add(new Obstacle(obstacleX, obstacleY, obstacleDx, obstacleDy));
        }

        setPreferredSize(new Dimension(SCREEN_WIDTH, SCREEN_HEIGHT));
        setBackground(BG_COLOR);
        addKeyListener(this);
        setFocusable(true);
    }

    @Override
    public void addNotify() {
        super.addNotify();
        Thread animator = new Thread(this);
        animator.start();
    }

    @Override
    public void run() {
        while (true) {
            update();
            repaint();
            try {
                Thread.sleep(1000 / FPS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void update() {
        // Update obstacles
        for (Obstacle obstacle : obstacles) {
            obstacle.update();

            // Check collision with screen edges for obstacle
            if (obstacle.getX() <= 0 || obstacle.getX() >= SCREEN_WIDTH - OBSTACLE_SIZE) {
                obstacle.reverseX();
            }
            if (obstacle.getY() >= SCREEN_HEIGHT) { // If obstacle falls below the screen, respawn at the top
                obstacle.respawn();
            }

            // Check collision between dot and obstacle
            if (dotX + DOT_SIZE >= obstacle.getX() && dotX <= obstacle.getX() + OBSTACLE_SIZE &&
                dotY + DOT_SIZE >= obstacle.getY() && dotY <= obstacle.getY() + OBSTACLE_SIZE) {
                gameOver();
            }
        }

        // Check key states for arrow keys
        if (keys[KeyEvent.VK_LEFT]) {
            dotX -= dotSpeed;
        } else if (keys[KeyEvent.VK_RIGHT]) {
            dotX += dotSpeed;
        }
        if (keys[KeyEvent.VK_UP]) {
            dotY -= dotSpeed;
        } else if (keys[KeyEvent.VK_DOWN]) {
            dotY += dotSpeed;
        }

        // Increment score (you can adjust scoring logic as per your game rules)
        score++;
    }

    private void gameOver() {
        System.out.println("Game Over!");
        System.exit(0);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Draw obstacles
        for (Obstacle obstacle : obstacles) {
            g.setColor(OBSTACLE_COLOR);
            g.fillRect(obstacle.getX(), obstacle.getY(), OBSTACLE_SIZE, OBSTACLE_SIZE);
        }

        // Draw the dot (player)
        g.setColor(DOT_COLOR);
        g.fillOval(dotX, dotY, DOT_SIZE, DOT_SIZE);

        // Draw score
        g.setColor(SCORE_COLOR);
        g.setFont(new Font("Arial", Font.PLAIN, 20));
        g.drawString("Score: " + score, 10, 20);
    }

    // KeyListener methods
    private boolean[] keys = new boolean[256];

    @Override
    public void keyPressed(KeyEvent e) {
        keys[e.getKeyCode()] = true;
    }

    @Override
    public void keyReleased(KeyEvent e) {
        keys[e.getKeyCode()] = false;
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Dot Game");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setContentPane(new DotGame());
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }

    // Inner class for obstacle
    private class Obstacle {
        private int x, y, dx, dy;

        public Obstacle(int x, int y, int dx, int dy) {
            this.x = x;
            this.y = y;
            this.dx = dx;
            this.dy = dy;
        }

        public int getX() {
            return x;
        }

        public int getY() {
            return y;
        }

        public void update() {
            x += dx;
            y += dy;
        }

        public void reverseX() {
            dx = -dx;
        }

        public void respawn() {
            x = new Random().nextInt(SCREEN_WIDTH - OBSTACLE_SIZE);
            y = new Random().nextInt(-SCREEN_HEIGHT - OBSTACLE_SIZE);
            dy = new Random().nextInt(3) + 1;
        }
    }
}
