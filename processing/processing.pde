import processing.video.*;
import oscP5.*;
Capture cam;
OscP5 oscP5;
float temperature = 0;
float utilization = 0;
float memoryUsed = 0;
float memoryTotal = 0;
float powerDraw = 0;
float powerTarget = 0;
String currentPrompt = "";
PGraphics camBuffer; // Buffer for camera texture
PGraphics prevBuffer; // Buffer for previous frame
float lerpAmount = 0; // Lerp progress
float lerpSpeed = 0.03; // Speed of transition

void setup() {
  fullScreen(P3D, 1);

  String[] cameras = Capture.list();
  println("Available cameras:");
  printArray(cameras);

  println(width, height);
  // The camera can be initialized directly using an element
  // from the array returned by list():
  cam = new Capture(this, cameras[1]);
  cam.start();
  hint(DISABLE_DEPTH_TEST);

  // Create buffers for camera and previous frame
  camBuffer = createGraphics(width, height, P2D);
  prevBuffer = createGraphics(width, height, P2D);

  // Initialize OSC and listen on port 12000
  oscP5 = new OscP5(this, 12000);
}

void draw() {
  background(0);

  // Update camera buffer
  if (cam.available() == true) {
    // Store current frame in prevBuffer before updating
    prevBuffer.beginDraw();
    prevBuffer.clear(); // Clear previous content
    prevBuffer.imageMode(CENTER);
    prevBuffer.image(camBuffer, width/2, height/2);
    prevBuffer.endDraw();

    cam.read();
    camBuffer.beginDraw();
    camBuffer.clear(); // Clear previous content
    camBuffer.imageMode(CENTER);
    camBuffer.image(cam, width/2, height/2, width*1.775, height);
    camBuffer.endDraw();

    // Reset lerp for new transition
    lerpAmount = 0;
  }

  // Display interpolated camera buffer
  imageMode(CENTER);
  if (lerpAmount < 1) {
    // Use blend() for smooth transition between frames
    lerpAmount = min(1, lerpAmount + lerpSpeed);
    blend(prevBuffer, 0, 0, width, height,
      0, 0, width, height, // Simplified coordinates
      BLEND);
    blend(camBuffer, 0, 0, width, height,
      0, 0, width, height, // Simplified coordinates
      MULTIPLY);
  } else {
    // Just show current frame when lerp is complete
    image(camBuffer, width/2, height/2);
  }

  textAlign(LEFT, CENTER);
  float baseTextSize = 20;
  float pulseAmount = 2;
  float pulse = abs(sin(radians(frameCount % 360))); // Prevent overflow

  // Display all GPU stats with color coding based on temperature
  textSize(baseTextSize + pulseAmount * pulse);

  // Color coding: green < 50°C, yellow 50-75°C, red > 75°C
  if (temperature < 50) {
    fill(0, 255, 0);
  } else if (temperature < 75) {
    fill(255, 255, 0);
  } else {
    fill(255, 0, 0);
  }

  text("GPU Temperature: " + nf(temperature, 0, 1) + "°C", width*0.05, height*0.05);

  // Reset color to white for other stats
  fill(255);
  text("GPU Utilization: " + nf(utilization, 0, 1) + "%", width*0.05, height*0.1);
  text("Memory: " + nf(memoryUsed/1024, 0, 1) + "/" + nf(memoryTotal/1024, 0, 1) + " GB", width*0.05, height*0.15);
  text("Power: " + nf(powerDraw, 0, 1) + "/" + nf(powerTarget, 0, 1) + " W", width*0.05, height*0.2);

  // Display current prompt if available
  if (currentPrompt != null && currentPrompt.length() > 0) {
    textSize(baseTextSize * 1.2);
    textAlign(LEFT, CENTER);
    text(currentPrompt, width/2, height*0.7, width*0.42, height*0.3);
  }

  // Run garbage collection every 300 frames to manage memory
  if (frameCount % 300 == 0) {
    System.gc();
  }
}

void dispose() {
  // Clean up resources when sketch is closed
  if (cam != null) {
    cam.stop();
  }
  if (camBuffer != null) {
    camBuffer.dispose();
  }
  if (prevBuffer != null) {
    prevBuffer.dispose();
  }
  if (oscP5 != null) {
    oscP5.stop();
  }
}

// OSC message received
void oscEvent(OscMessage msg) {
  if (msg == null) return;

  if (msg.checkAddrPattern("/gpu/temperature")) {
    temperature = msg.get(0).floatValue();
  } else if (msg.checkAddrPattern("/gpu/utilization")) {
    utilization = msg.get(0).floatValue();
  } else if (msg.checkAddrPattern("/gpu/memory_used")) {
    memoryUsed = msg.get(0).floatValue();
  } else if (msg.checkAddrPattern("/gpu/memory_total")) {
    memoryTotal = msg.get(0).floatValue();
  } else if (msg.checkAddrPattern("/gpu/power_draw")) {
    powerDraw = msg.get(0).floatValue();
  } else if (msg.checkAddrPattern("/gpu/power_target")) {
    powerTarget = msg.get(0).floatValue();
  } else if (msg.checkAddrPattern("/prompt")) {
    currentPrompt = msg.get(0).stringValue();
  }
}
