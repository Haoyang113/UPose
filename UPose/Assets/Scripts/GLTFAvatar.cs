
using UnityEngine;
using GLTFast;
using System.Linq;

public class Avatar : MonoBehaviour
{

    private MotionTracking server;

    private Transform Hips;
    private Transform Spine;
    private Transform LeftUpLeg;
    private Transform LeftLeg;
    private Transform RightUpLeg;
    private Transform RightLeg;
    private Transform LeftArm;
    private Transform LeftForeArm;
    private Transform RightArm;
    private Transform RightForeArm;

    private bool AVATAR_LOADED=false;

    private void Start()
    {

        server = FindObjectOfType<MotionTracking>();
        if (server == null)
        {
            Debug.LogError("You must have a Pipeserver in the scene!");
        }

        InitializeAvatar();

    }

    private async void InitializeAvatar(){
        var gltfImport = new GltfImport();
        await gltfImport.Load("https://digitalworlds.github.io/UPose/Assets/Soldier.glb");
        var instantiator = new GameObjectInstantiator(gltfImport,transform);
        var success = await gltfImport.InstantiateMainSceneAsync(instantiator);
        if (success) {
            Debug.Log("GLTF file is loaded.");
        
            
            Hips = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:Hips");
            Spine = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:Spine");
            
            LeftUpLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:LeftUpLeg");
            LeftLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:LeftLeg");
            
            RightUpLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:RightUpLeg");
            RightLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:RightLeg");
            
            LeftArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:LeftArm");
            LeftForeArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:LeftForeArm");
            
            RightArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:RightArm");
            RightForeArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "mixamorig:RightForeArm");
            
            
            AVATAR_LOADED=true;

        }else{
            Debug.Log("ERROR: GLTF file is NOT loaded!");
        }
    }

    private void Update()
    {
        
        Hips.localRotation=server.GetRotation(Landmark.PELVIS);
        
        Spine.localRotation=server.GetRotation(Landmark.SHOULDER_CENTER);
       
        
        RightArm.localRotation=server.GetRotation(Landmark.RIGHT_SHOULDER);
        RightArm.Rotate(0,90,0);
        Vector3 angles=RightArm.localRotation.eulerAngles;
        RightArm.localRotation = Quaternion.Euler(90-angles.y, angles.z,-angles.x);
        
        LeftArm.localRotation=server.GetRotation(Landmark.LEFT_SHOULDER);
        LeftArm.Rotate(0,-90,0);
        angles=LeftArm.localRotation.eulerAngles;
        LeftArm.localRotation = Quaternion.Euler(-90-angles.y, 0,-angles.x);

        /*LeftForeArm.localRotation=Quaternion.Inverse(server.GetLandmark(Landmark.LEFT_SHOULDER).localRotation)*server.GetLandmark(Landmark.LEFT_ELBOW).localRotation;
        angles =LeftForeArm.localRotation.eulerAngles;
        LeftForeArm.localRotation = Quaternion.Euler(-180+server.getLeftElbowAngle(), 0, 0); ;

        RightForeArm.localRotation=Quaternion.Inverse(server.GetLandmark(Landmark.RIGHT_SHOULDER).localRotation)*server.GetLandmark(Landmark.RIGHT_ELBOW).localRotation;
        angles =RightForeArm.localRotation.eulerAngles;
        RightForeArm.localRotation = Quaternion.Euler(-180-server.getRightElbowAngle(), 0, 0); ;
        */

        LeftForeArm.localRotation=server.GetRotation(Landmark.LEFT_ELBOW);
        angles=LeftForeArm.localRotation.eulerAngles;
        LeftForeArm.localRotation = Quaternion.Euler(-angles.y, 0,0);

        RightForeArm.localRotation=server.GetRotation(Landmark.RIGHT_ELBOW);
        angles=RightForeArm.localRotation.eulerAngles;
        RightForeArm.localRotation = Quaternion.Euler(-angles.y, 0,0);


        RightUpLeg.localRotation=server.GetRotation(Landmark.RIGHT_HIP);
        angles=RightUpLeg.localRotation.eulerAngles;
        RightUpLeg.localRotation = Quaternion.Euler(-180+angles.x, angles.y,-angles.z); 
        
        LeftUpLeg.localRotation=server.GetRotation(Landmark.LEFT_HIP);
        angles=LeftUpLeg.localRotation.eulerAngles;
        LeftUpLeg.localRotation = Quaternion.Euler(-180+angles.x, angles.y,-angles.z);    
        
        LeftLeg.localRotation=server.GetRotation(Landmark.LEFT_KNEE);
        RightLeg.localRotation=server.GetRotation(Landmark.RIGHT_KNEE);
    }

}
