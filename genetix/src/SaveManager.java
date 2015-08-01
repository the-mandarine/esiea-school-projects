import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.ListIterator;

/*
 * SaveManager.java
 * Component of GenetiX UAV
 * 
 * This class is designed to manage a save file that keeps the best results
 * previously calculated by the algorithm
 * 
 * @version 1.0
 * @author Timothee Duval & Franklin Raccah
 * 
 */


public class SaveManager {
	String saveFile;
	ArrayList<String> file;
	public SaveManager(){
		
	}

	public SaveManager(String configFile) throws IOException {
		fileManage(configFile);
		saveFile = configFile;
		file = new ArrayList<String>();
		
		FileInputStream finStream = new FileInputStream(saveFile);
		DataInputStream in = new DataInputStream(finStream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in));
		String buff;
		while ((buff = br.readLine()) != null) {
			file.add(buff);
		}
	}
	
	public float[] getPreviousBest(String mission, String uav, float result, float[] coefs) throws IOException{
		float[] ret = new float[6];

		ListIterator<String> iter = file.listIterator();
		
		String buff;
		String[] tmpbuff;
		int ligne = 0;
		int final_ligne = -1;
		while (iter.hasNext()){
			buff = iter.next();
			ligne++;
			tmpbuff = buff.split(";");
			if(tmpbuff[0].equals(mission) && tmpbuff[1].equals(uav)){
				if(Float.parseFloat(tmpbuff[2])<=result)
				{
					for(int i=0;i<6;i++)
					{
						ret[i] = Float.parseFloat(tmpbuff[3+i]);
					}
					return ret;
				}
				else{
					final_ligne = ligne;
				}
			}
		}
		
		// Si les resultats n'existent pas ou sont moins bon on les �crit
		if(final_ligne != -1){
			file.remove(final_ligne-1);
		}
		else{
			final_ligne = 1;
		}
		String newlign = mission + ";" + uav + ";" + result + ";";
		for(int i = 0; i<5 ; i++)
		{
			newlign += coefs[i] + ";";
		}
		newlign += coefs[5];
		file.add(final_ligne-1, newlign);
		ListIterator<String> iter2 = file.listIterator();
		
		File fich = new File(saveFile);
		fich.delete();
		fich.createNewFile();
		FileWriter oStream = new FileWriter(saveFile);
		BufferedWriter out = new BufferedWriter(oStream);
		while(iter2.hasNext())
		{
			buff=iter2.next();
			out.write(buff+"\n");
		}
		out.close();
		return coefs;
	}
	
	private void fileManage(String filename){
		File tmp = new File(filename);
		if(!tmp.exists())
		{
			try {
				tmp.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
