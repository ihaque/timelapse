PImage img;
float rot = 3*PI/2;
float lineY = 0;
int frameno = 0;
int breakidx = 0;
String[] filenames; 
int[] framenumbers;
PFont font;

void setup() {
  size(600,800);
  String[] lines = loadStrings("FILE NAME HERE");
  filenames = new String[lines.length];
  framenumbers = new int[lines.length];
  for (int i = 0; i < lines.length; i++) {
    String[] fields = split(lines[i],',');
    filenames[i] = fields[0];
    framenumbers[i] = int(fields[1]);
  }
  font=loadFont("ArialMT-48.vlw");
  textFont(font);
  loadbreak();
}
void loadbreak() {
    img = loadImage(filenames[breakidx]);
    img.resize(800,600);
    lineY=0;
}
void draw() {
  background(255);
  translate(width/2,height/2);
  rotate(rot);
  image(img,-img.width/2,-img.height/2);
  rotate(-rot);
  translate(-width/2,-height/2);
  stroke(255,0,0);
  line(0,lineY,600,lineY);
  fill(255,0,0);
  textAlign(RIGHT);
  text(""+(breakidx+1)+"/"+filenames.length,600,50);
}
void mouseClicked() {
  lineY=mouseY;
}
void mouseDragged() {
  lineY=mouseY;
}
void keyPressed() {
  if (key == 'd' || key == 'D') {
    print("del "+framenumbers[breakidx] + " " + framenumbers[breakidx]+"\n");
  } else {
    print("crop "+framenumbers[breakidx]+" "+(int)(2*lineY)+"\n");
  }
  breakidx++;
  if (breakidx == filenames.length) {
    print("Done!\n");
    exit();
  } else {
    loadbreak();
  }
}
