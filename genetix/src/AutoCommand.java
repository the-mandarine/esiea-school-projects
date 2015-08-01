import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

import uavPhysicalSimulator.PhysicalTestBox;
import uavPhysicalSimulator.ThrustCommand;

/*
 * 
 * AutoCommand.java
 * Compoment of GenetiX UAV
 * 
 * This class implements the auto-command algorithm
 * 
 * It requires a mission file, a uav descriptor file and a configuration file
 * 
 * @version 1.0
 * @author Timothee Duval & Franklin Raccah
 */


public class AutoCommand  {
	int nb_random_report_gen = 100;

	Config config;
	AnonymCommand ret;
	PhysicalTestBox mission;
	UAVThing uav;
	String missionFile;
	String uavFile;
	boolean use_save;

	public AutoCommand(String missionFile, String uavFile, String conf, boolean use_save) throws IOException
	{
		if(!missionFile.isEmpty() && !uavFile.isEmpty())
		{
			uav = new UAVThing(uavFile);
			mission = new PhysicalTestBox(missionFile, uavFile);

		}
		this.missionFile = missionFile;
		this.uavFile = uavFile;
		this.use_save = use_save;
		config = new Config(conf);
	}

	public ThrustCommand getBestCommand()
	{
		selectValues();
		return ret;
	}


	// Finding coeffs
	private void selectValues()
	{
		ArrayList<Float> popVals = new ArrayList<Float>();
		ArrayList<Float> sortedPopVals = new ArrayList<Float>();

		float[] curParent;
		int j;


		ArrayList<float[]> coeffsParents = new ArrayList<float[]>();
		ArrayList<float[]> coeffsBestParents = new ArrayList<float[]>();

		// Initializing population and calculating their values
		int nbParents = config.nbParentsInitial;


		Random random_seed = new Random(System.currentTimeMillis());

		for(int i = 0 ; i < nbParents; i++)
		{
			// DO NOT attempt to factorize that
			float[] newParent = new float[6];

			for(int k = 0 ; k < 6 ; k++) {
				newParent[k] = random_seed.nextFloat() * config.agressivity;
			}

			coeffsParents.add(newParent);
		}


		for (int iterations = 0; iterations < config.nbMutations; iterations++)
		{       
			// Evaluating coefficients in coeffsParents
			for (int i = 0 ; i < nbParents ; i++){
				Float eval_result = mission.evaluate(
						new AnonymCommand(uav.getWeight(), coeffsParents.get(i)[0],coeffsParents.get(i)[1],
								coeffsParents.get(i)[2], coeffsParents.get(i)[3], 
								coeffsParents.get(i)[4], coeffsParents.get(i)[5]));

				if (i % config.nbParentsPerGeneration == 0) {
					System.err.println(((float)iterations / config.nbMutations * 100) + "%... ");
				}

				popVals.add(eval_result);

			}

			sortedPopVals.addAll(popVals);
			Collections.sort(sortedPopVals);

			nbParents = config.nbParentsPerGeneration;

			//System.err.println(sortedPopVals.get(0));
			// Taking the best parents
			for (int i = 0 ; i < nbParents ; i++) {
				curParent = coeffsParents.get(popVals.indexOf(sortedPopVals.get(i)));
				coeffsBestParents.add(curParent);
			}

			popVals.clear();
			sortedPopVals.clear();
			coeffsParents.clear();

			// Make children
			int iter = nbParents * nbParents;

			coeffsParents.add(coeffsBestParents.get(0));

			for (int i = 1 ; i < iter ; i++){
				float[] newChild = new float[6];
				newChild[0] = coeffsBestParents.get(random_seed.nextInt(nbParents))[0];
				newChild[1] = coeffsBestParents.get(random_seed.nextInt(nbParents))[1];
				newChild[2] = coeffsBestParents.get(random_seed.nextInt(nbParents))[2];
				newChild[3] = coeffsBestParents.get(random_seed.nextInt(nbParents))[3];
				newChild[4] = coeffsBestParents.get(random_seed.nextInt(nbParents))[4];
				newChild[5] = coeffsBestParents.get(random_seed.nextInt(nbParents))[5];

				coeffsParents.add(newChild);
			}

			coeffsBestParents.clear();

			// Mutate everything except the best parent
			mutate(coeffsParents, nbParents);
		}


		// Evaluating the best of bests
		int iter = nbParents*nbParents;

		for (int i = 0 ; i < iter ; i++){
			curParent = coeffsParents.get(i);
			popVals.add(mission.evaluate(
					new AnonymCommand(uav.getWeight(), curParent[0], curParent[1], 
							curParent[2], curParent[3], 
							curParent[4], curParent[5])));

		}

		sortedPopVals.addAll(popVals);

		Collections.sort(sortedPopVals);


		j = popVals.indexOf(sortedPopVals.get(0));

		if (use_save){
			// Checks if result is better than previous result if it exists  replaces current result by saved one if worse
			try {

				SaveManager save = new SaveManager("./cfg/save.dat");
				float[] temp = new float[6];
				temp = save.getPreviousBest(missionFile, 
						uavFile, 
						mission.evaluate(new AnonymCommand(uav.getWeight(), 
								coeffsParents.get(j)[0],coeffsParents.get(j)[1], 
								coeffsParents.get(j)[2],coeffsParents.get(j)[3], 
								coeffsParents.get(j)[4],coeffsParents.get(j)[5])), 
								coeffsParents.get(j));
				coeffsParents.remove(j);
				coeffsParents.add(j, temp);
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		System.err.println("Coefficients : ");
		for (int i = 0 ; i < 6 ; i++){
			System.out.print(uav.getWeight());
			System.out.print(" "+coeffsParents.get(j)[i]);
		}
		System.out.println();
		ret = new AnonymCommand(uav.getWeight(), coeffsParents.get(j)[0],coeffsParents.get(j)[1], 
				coeffsParents.get(j)[2],coeffsParents.get(j)[3], 
				coeffsParents.get(j)[4],coeffsParents.get(j)[5]);

	}

	private void mutate(ArrayList<float[]> in, int nb) {
		float mutation;
		float cur_in;
		Random random_seed = new Random(System.currentTimeMillis());

		for (int i = 1 ; i < nb ; i++){
			for (int j = 0 ; j < 6 ; j++){
				cur_in = in.get(i)[j];
				mutation = ((random_seed.nextFloat() - (float)0.5)) * config.agentXConcentration;
				in.get(i)[j] += mutation * cur_in;
			}
		}
	}
}
