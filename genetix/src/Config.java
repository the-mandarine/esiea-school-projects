import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import com.google.gson.Gson;


public class Config {
	
	int nbParentsInitial;
	int nbParentsPerGeneration;
	int nbMutations;
	float agentXConcentration;
	int agressivity;
	String missionFile;
	String uavFile;
	
	public Config(){
		
	}
	
	public Config(String configFile) throws IOException {
		String json = getFullJson(configFile);
		Gson gson = new Gson();
		Config conf = new Config();
		conf = gson.fromJson(json, Config.class);
		this.update(conf);
	}
	
	private void update(Config conf){
		this.agentXConcentration = conf.agentXConcentration;
		this.agressivity = conf.agressivity;
		this.nbMutations = conf.nbMutations;
		this.nbParentsInitial = conf.nbParentsInitial;
		this.nbParentsPerGeneration = conf.nbParentsPerGeneration;
		this.uavFile = conf.uavFile;
		this.missionFile = conf.missionFile;
	}
	
	private String getFullJson(String uavFile) throws IOException{
		FileInputStream finStream = new FileInputStream(uavFile);
		DataInputStream in = new DataInputStream(finStream);
		BufferedReader br = new BufferedReader(new InputStreamReader(in));
		String full_json = new String();
		String buff_json;
		while ((buff_json = br.readLine()) != null) {
			full_json += buff_json+"\n";
		}
		return full_json;
	}
	
	public int getNbParentsInitial() {
		return nbParentsInitial;
	}
	public int getNbParentsPerGeneration() {
		return nbParentsPerGeneration;
	}
	public int getNbMutations() {
		return nbMutations;
	}
	public float getAgentXConcentration() {
		return agentXConcentration;
	}
	public int getAgressivity() {
		return agressivity;
	}
	public String getMissionFile() {
		return missionFile;
	}
	public String getUavFile() {
		return uavFile;
	}
	
	
}
