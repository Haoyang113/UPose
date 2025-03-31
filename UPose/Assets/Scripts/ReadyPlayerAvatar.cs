
using UnityEngine;
using GLTFast;
using System.Linq;
using System.Xml.Serialization;
using System;

public class ReadyPlayerAvatar : MonoBehaviour
{

    private MotionTracking server;

    private Transform Hips;
    private Transform Spine;
    private Transform LeftUpLeg;
    private Transform LeftLeg;
    private Transform RightUpLeg;
    private Transform RightLeg;
    private Transform LeftShoulder;
    private Transform LeftArm;
    private Transform LeftForeArm;
    private Transform RightShoulder;
    private Transform RightArm;
    private Transform RightForeArm;

    private bool AVATAR_LOADED=false;

    public enum AvatarChoice { FemaleGymClothing, FemaleDress,FemaleCasual, MaleCasual, MaleTshirt, MaleArmored}
    public AvatarChoice avatar;

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
        String avatar_url="";
        switch (avatar)
        {
            case AvatarChoice.FemaleGymClothing:
                avatar_url="avatar.glb";
                break;
            case AvatarChoice.FemaleDress:
                avatar_url="avatar1.glb";
                break;
            case AvatarChoice.FemaleCasual:
                avatar_url="67e20a7fc5f8c4a77988b853.glb";
                break;
            case AvatarChoice.MaleCasual:
                avatar_url= "67d411b30787acbf58ce58ac.glb";
                break;
            case AvatarChoice.MaleTshirt:
                avatar_url="67e21d1a79ac9bcf81a46385.glb";
                break;
            case AvatarChoice.MaleArmored:
                avatar_url="67e21f3db6349f1f57421ba0.glb";
                break;
            default:
                avatar_url="avatar.glb";
                break;
        }

        await gltfImport.Load("https://digitalworlds.github.io/UPose/Assets/"+avatar_url);
        var instantiator = new GameObjectInstantiator(gltfImport,transform);
        var success = await gltfImport.InstantiateMainSceneAsync(instantiator);
        if (success) {
            Debug.Log("GLTF file is loaded.");
        
            
            Hips = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "Hips");
            Spine = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "Spine");
            Transform Spine1 = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "Spine1");
            Spine1.localRotation=Quaternion.Euler(0,0,0);
            Transform Spine2 = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "Spine2");
            Spine2.localRotation=Quaternion.Euler(0,0,0);

            LeftUpLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftUpLeg");
            LeftLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftLeg");
            
            RightUpLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightUpLeg");
            RightLeg = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightLeg");
            
            Transform LeftFoot=GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftFoot");
            
            GameObject colliderHolder = new GameObject("LeftFootCollider");
            colliderHolder.transform.SetParent(LeftFoot);
            colliderHolder.transform.localPosition = new Vector3(0, 0.125f, 0);
            colliderHolder.transform.localRotation = Quaternion.Euler(-55,0,0);
            Rigidbody rb=colliderHolder.AddComponent<Rigidbody>();
            rb.isKinematic=true;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
            BoxCollider footCollider = colliderHolder.AddComponent<BoxCollider>();
            footCollider.size = new Vector3(0.15f, 0.1f, 0.3f);
            colliderHolder.AddComponent<KickForce>();


            Transform RightFoot=GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightFoot");
        
            colliderHolder = new GameObject("RightFootCollider");
            colliderHolder.transform.SetParent(RightFoot);
            colliderHolder.transform.localPosition = new Vector3(0, 0.125f, 0);
            colliderHolder.transform.localRotation = Quaternion.Euler(-55,0,0);
            rb=colliderHolder.AddComponent<Rigidbody>();
            rb.isKinematic=true;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
            footCollider = colliderHolder.AddComponent<BoxCollider>();
            footCollider.size = new Vector3(0.15f, 0.1f, 0.3f);
            colliderHolder.AddComponent<KickForce>();

            LeftShoulder = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftShoulder");
            
            LeftArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftArm");
            LeftArm.localRotation=Quaternion.Euler(0,0,0);
            LeftForeArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftForeArm");
            
            Transform LeftHand=GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "LeftHand");
        
            colliderHolder = new GameObject("LeftHandCollider");
            colliderHolder.transform.SetParent(LeftHand);
            colliderHolder.transform.localPosition = new Vector3(0, 0.1f, 0);
            colliderHolder.transform.localRotation = Quaternion.Euler(-90,0,0);
            rb=colliderHolder.AddComponent<Rigidbody>();
            rb.isKinematic=true;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
            footCollider = colliderHolder.AddComponent<BoxCollider>();
            footCollider.size = new Vector3(0.15f, 0.1f, 0.2f);
            colliderHolder.AddComponent<KickForce>();

            RightShoulder = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightShoulder");
            
            RightArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightArm");
            RightArm.localRotation=Quaternion.Euler(0,0,0);
            RightForeArm = GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightForeArm");
            
            Transform RightHand=GetComponentsInChildren<Transform>(true).FirstOrDefault(t => t.name == "RightHand");
        
            colliderHolder = new GameObject("RightHandCollider");
            colliderHolder.transform.SetParent(RightHand);
            colliderHolder.transform.localPosition = new Vector3(0, 0.1f, 0);
            colliderHolder.transform.localRotation = Quaternion.Euler(-90,0,0);
            rb=colliderHolder.AddComponent<Rigidbody>();
            rb.isKinematic=true;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
            footCollider = colliderHolder.AddComponent<BoxCollider>();
            footCollider.size = new Vector3(0.15f, 0.1f, 0.2f);
            colliderHolder.AddComponent<KickForce>();
            
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
        RightShoulder.localRotation=server.GetRotation(Landmark.RIGHT_SHOULDER);
        //Get left upper arm rotation and apply it to the avatar
        LeftShoulder.localRotation=server.GetRotation(Landmark.LEFT_SHOULDER);
        //Get left fore arm rotation and apply it to the avatar
        LeftForeArm.localRotation=server.GetRotation(Landmark.LEFT_ELBOW);
        //Get right fore arm rotation and apply it to the avatar
        RightForeArm.localRotation=server.GetRotation(Landmark.RIGHT_ELBOW);
        //Get right thigh arm rotation and apply it to the avatar  
        RightUpLeg.localRotation=server.GetRotation(Landmark.RIGHT_HIP);
        //Get left thigh rotation and apply it to the avatar
        LeftUpLeg.localRotation=server.GetRotation(Landmark.LEFT_HIP);
        //Get left leg rotation and apply it to the avatar
        LeftLeg.localRotation=server.GetRotation(Landmark.LEFT_KNEE);
        //Get right leg rotation and apply it to the avatar
        RightLeg.localRotation=server.GetRotation(Landmark.RIGHT_KNEE);


        //server.MoveToFloor(this,-1);
    }

}
