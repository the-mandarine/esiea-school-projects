import uavPhysicalSimulator.Thrust;
import uavPhysicalSimulator.ThrustCommand;


public class AnonymCommand implements ThrustCommand {
        float stableValue;
        float x1,x2,y1,y2,a1,a2;
        public AnonymCommand(float stability,float x1, float x2, float y1, float y2, float a1, float a2) {
                this.stableValue = stability;
                this.x1 = x1;
                this.x2 = x2;
                this.y1 = y1;
                this.y2 = y2;
                this.a1 = a1;
                this.a2 = a2;
        }

        public Thrust getThrust(float xDistance, float yDistance, float a, float dx,
                        float dy, float da) {
                double leftThrust=0;
                double rightThrust = 0;
                double xCor,yCor,aCor;
                xCor = x1*xDistance - x2*dx;
                yCor = y1*yDistance - y2*dy;
                aCor = a1*a - a2*da;
                leftThrust = stableValue + yCor + xCor - aCor;
                rightThrust = stableValue + yCor - xCor + aCor;

                return new Thrust((float)leftThrust,(float)rightThrust);
        }

}