import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import com.google.gson.Gson;


public class UAVThing {
	private float weight;
	private float[][] pt;
	private float density;
	private float gravitation = (float)10.00;
	
	public UAVThing(){
		
	}
	public UAVThing(String uavFile) throws IOException {
		String json = getFullJson(uavFile);
		Gson gson = new Gson();
		UAVThing uav = new UAVThing();
		uav = gson.fromJson(json, UAVThing.class);

		setWeight(uav.pt, uav.density);
		
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
	
	private void setWeight(float[][] pts, float density){
		weight = 0;
		for (int i = 0 ; i < pts.length ; i++){
			weight += pts[i][0] * pts[(i+1) % pts.length][1];
			weight -= pts[i][1] * pts[(i+1) % pts.length][0];
		}
	}
	
	public float getWeight(){
		return weight * gravitation;
	}
}
