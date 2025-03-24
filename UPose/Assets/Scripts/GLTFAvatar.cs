
using UnityEngine;
using GLTFast;
using System.Linq;

public class GLTFAvatar : MonoBehaviour
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

        server = FindFirstObjectByType<MotionTracking>();
        if (server == null)
        {
            Debug.LogError("You must have a Pipeserver in the scene!");
        }

        InitializeAvatar();

    }

    private async void InitializeAvatar(){
        var gltfImport = new GltfImport();
        await gltfImport.Load("https://digitalworlds.github.io/UPose/Assets/67d411b30787acbf58ce58ac.glb");
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
        if(!AVATAR_LOADED)return;

        //Get pelvis local rotation and apply it to the avatar
        Hips.localRotation=server.GetRotation(Landmark.PELVIS);
        
        //Get torso local rotation and apply it to the avatar
        Spine.localRotation=server.GetRotation(Landmark.SHOULDER_CENTER);
       
        //Get right upper arm rotation and apply it to the avatar
        RightArm.localRotation=server.GetRotation(Landmark.RIGHT_SHOULDER);
        //Modify the coordinate system if necessary according to your avatar
        RightArm.Rotate(0,90,0);
        Vector3 angles=RightArm.localRotation.eulerAngles;
        RightArm.localRotation = Quaternion.Euler(90-angles.y, angles.z,-angles.x);
        
        //Get left upper arm rotation and apply it to the avatar
        LeftArm.localRotation=server.GetRotation(Landmark.LEFT_SHOULDER);
        //Modify the coordinate system if necessary according to your avatar        
        LeftArm.Rotate(0,-90,0);
        angles=LeftArm.localRotation.eulerAngles;
        LeftArm.localRotation = Quaternion.Euler(-90-angles.y, 0,-angles.x);

        //Get left fore arm rotation and apply it to the avatar
        LeftForeArm.localRotation=server.GetRotation(Landmark.LEFT_ELBOW);
        //Modify the coordinate system if necessary according to your avatar
        angles=LeftForeArm.localRotation.eulerAngles;
        LeftForeArm.localRotation = Quaternion.Euler(-angles.y, 0,0);

        //Get right fore arm rotation and apply it to the avatar
        RightForeArm.localRotation=server.GetRotation(Landmark.RIGHT_ELBOW);
        //Modify the coordinate system if necessary according to your avatar
        angles=RightForeArm.localRotation.eulerAngles;
        RightForeArm.localRotation = Quaternion.Euler(-angles.y, 0,0);


        //Get right thigh arm rotation and apply it to the avatar  
        RightUpLeg.localRotation=server.GetRotation(Landmark.RIGHT_HIP);
        //Modify the coordinate system if necessary according to your avatar
        angles=RightUpLeg.localRotation.eulerAngles;
        RightUpLeg.localRotation = Quaternion.Euler(-180+angles.x, angles.y,-angles.z); 
        
        //Get left thigh rotation and apply it to the avatar
        LeftUpLeg.localRotation=server.GetRotation(Landmark.LEFT_HIP);
        //Modify the coordinate system if necessary according to your avatar
        angles=LeftUpLeg.localRotation.eulerAngles;
        LeftUpLeg.localRotation = Quaternion.Euler(-180+angles.x, angles.y,-angles.z);    
        
        //Get left leg rotation and apply it to the avatar
        LeftLeg.localRotation=server.GetRotation(Landmark.LEFT_KNEE);
        //Get right leg rotation and apply it to the avatar
        RightLeg.localRotation=server.GetRotation(Landmark.RIGHT_KNEE);



        /*LeftForeArm.localRotation=Quaternion.Inverse(server.GetLandmark(Landmark.LEFT_SHOULDER).localRotation)*server.GetLandmark(Landmark.LEFT_ELBOW).localRotation;
        angles =LeftForeArm.localRotation.eulerAngles;
        LeftForeArm.localRotation = Quaternion.Euler(-180+server.getLeftElbowAngle(), 0, 0); ;

        RightForeArm.localRotation=Quaternion.Inverse(server.GetLandmark(Landmark.RIGHT_SHOULDER).localRotation)*server.GetLandmark(Landmark.RIGHT_ELBOW).localRotation;
        angles =RightForeArm.localRotation.eulerAngles;
        RightForeArm.localRotation = Quaternion.Euler(-180-server.getRightElbowAngle(), 0, 0); ;
        */
    }

}
