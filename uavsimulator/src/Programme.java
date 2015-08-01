import java.io.IOException;

import javax.swing.JFrame;

import uavPhysicalSimulator.PhysicalTestBox;
import uavPhysicalSimulator.ThrustCommand;


public class Programme {
		
		private static void usage(){
			System.out.println("GenetiX UAV");
			System.out.println("usage :");
			System.out.println("\texecutable [-h | [ mission [ uav [ config [-s]]]]]");
			System.out.println("-h : print this help");
			System.out.println("-s : use saved results");
			System.out.println();
		}
        /**
         * @param args
         * @throws IOException 
         */
        public static void main(String[] args) throws IOException {
        		String conf = "./cfg/config01.json";
                String mission = "./cfg/mission01.json";
                String uav = "./cfg/uav01.json";
                boolean use_save = false;
                
                if(args.length > 0){
                	if (args.length == 1 && args[0].equals("-h"))
                	{
                		usage();
                		System.exit(0);
                	}
                	mission = args[0];
                }
                if(args.length > 1){
                	uav = args[1];
                }
                if(args.length > 2){
                	conf = args[2];
                }
                if(args.length > 3 && args[3].equals("-s")){
                	use_save = true;
                }
                if(args.length > 4){
                	usage();
                	System.exit(0);
                }
                
                
                AutoCommand calculator = new AutoCommand(mission, uav, conf, use_save);
                PhysicalTestBox testBox = new PhysicalTestBox(mission, uav);
                ThrustCommand command  = calculator.getBestCommand();

                JFrame frame = new JFrame("My Damn Simulator");
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                /* Addind components */
                frame.add(testBox.getDrawingPanel());

                frame.pack();
                frame.setVisible(true);
                
                testBox.show(command);


        }
}
