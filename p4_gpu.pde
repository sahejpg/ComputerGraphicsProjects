// This is the provided code for Project 4.  Your main task will be to modify the
// provided .frag and .vert shader programs to create various visual effects.

// Using the scroll wheel zooms the cards in and out.
// Pressing the space bar locks/unlocks the object's position.

// global variables
PShader floorShader;
PShader square_shader;
PShader fractal_shader;
PShader image_manip_shader;
PShader bumps_shader;
PImage sheep_texture;
PImage sheep_mask;

float offsetY;
float offsetX;
float zoom = -200;
boolean locked = false;
float dirY = 0;
float dirX = 0;
float time = 9;
float delta_time = 0.02;
float blur_flag = 0;

// initialize variables and load the shaders
void setup() {
  size(640, 640, P3D);
  frameRate(30);
  offsetX = width/2;
  offsetY = height/2;
  noStroke();
  fill(206);

  // load textures
  sheep_texture = loadImage("data/sheep.jpg");
  sheep_mask = loadImage("data/sheep_mask.jpg");

  // load shaders
  square_shader = loadShader("data/squares.frag", "data/squares.vert");
  fractal_shader = loadShader("data/fractal.frag", "data/fractal.vert");
  image_manip_shader = loadShader("data/image_manip.frag", "data/image_manip.vert");
  bumps_shader = loadShader("data/bumps.frag", "data/bumps.vert");

  // floor shader
  floorShader = loadShader("data/floor.frag", "data/floor.vert");
}

void draw() {

  background(0);

  // control the scene rotation using the current mouse location
  if (!locked) {
    dirY = (mouseY / float(height) - 0.5) * 2;
    dirX = (mouseX / float(width) - 0.5) * 2;
  }

  // update the camera location based on the mouse
  if (mousePressed) {
    offsetY += (mouseY - pmouseY);
    offsetX += (mouseX - pmouseX);
  }

  // create a single directional light
  directionalLight(190, 190, 190, 0, 0, -1);

  // translate and rotate all objects to simulate a camera
  // note: processing +y points DOWN
  translate(offsetX, offsetY, zoom);
  rotateY(-dirX * 1.5);
  rotateX(dirY);
  
  // Draw a floor plane with the default shader
  shader(floorShader);
  beginShape();
  vertex(-300, 300, -400);
  vertex( 300, 300, -400);
  vertex( 300, 300, 200);
  vertex(-300, 300, 200);
  endShape();
  

  // Use the fractal shader
  shader(fractal_shader);
  
  // pass the parameters cx and cy to the fractal shader
  float r = 0.2;
  float mx = 1.0;
  float my = 0.1;
  float cx = mx + r * sin(time);
  float cy = my + r * cos(time);
  fractal_shader.set ("cx", cx);
  fractal_shader.set ("cy", cy);
  
  textureMode(NORMAL);
  beginShape();
  vertex(50, 50, -300, 0, 0);
  vertex(300, 50, -300, 1, 0);
  vertex(300, 300, -300, 1, 1);
  vertex(50, 300, -300, 0, 1);
  endShape();

  // use the image manipulation shader
  image_manip_shader.set("my_texture", sheep_texture);
  image_manip_shader.set("my_mask", sheep_mask);
  image_manip_shader.set ("blur_flag", blur_flag);
  shader(image_manip_shader);
  textureMode(NORMAL);
  beginShape();
  texture(sheep_texture);
  texture(sheep_mask);
  vertex(-300, 50, 100, 0, 0);
  vertex(-50, 50, 100, 1, 0);
  vertex(-50, 300, 100, 1, 1);
  vertex(-300, 300, 100, 0, 1);
  endShape();
  
  // use the bumps shader
  shader(bumps_shader);
  pushMatrix();
  translate (-300, 0, -300);
  float quad_size = 5.0;
  float N = 50.0;
  for (int i = 0; i <= N; i++) {
    for (int j = 0; j <= N; j++) {
      beginShape();
      texture(sheep_texture);
      vertex(50 + i * quad_size, 50 + j * quad_size, 0, (i/N), (j/N));
      vertex(50 + (i + 1) * quad_size, 50 + j * quad_size, 0, (i + 1)/ N, j/N);
      vertex(50 + (i + 1) * quad_size, 50 + (j + 1) * quad_size, 0, (i + 1)/N, (j + 1)/ N);
      vertex(50 + i * quad_size, 50 + (j + 1) * quad_size, 0, (i/N), (j + 1)/ N);
      endShape();
    }
  }
  popMatrix();

  // use the squares shader
  shader(square_shader);
  beginShape();
  vertex(50, 50, 100, 0, 0);
  vertex(300, 50, 100, 1, 0);
  vertex(300, 300, 100, 1, 1);
  vertex(50, 300, 100, 0, 1);
  endShape();

  // update the time variable
  time += delta_time;
}

void keyPressed() {
  if (key == ' ') {
    locked = !locked;
  }
  if (key == 'b') {
    blur_flag = 1 - blur_flag;
  }
}

void mouseWheel(MouseEvent event) {
  zoom += event.getAmount() * 12.0;
}
