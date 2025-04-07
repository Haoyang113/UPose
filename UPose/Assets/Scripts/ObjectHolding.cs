using UnityEngine;

public class ObjectHolding : MonoBehaviour
{
    ReadyPlayerAvatar avatar;
    bool initialized=false;
    LineRenderer line;
    GameObject topBox;
    GameObject bottomBox;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        avatar = GetComponent<ReadyPlayerAvatar>();
    }

    // Update is called once per frame
    void Update()
    {
        if(!initialized && avatar.isLoaded()){
            Debug.Log("Cylinder added");
            GameObject left_hand=avatar.getLeftHand();
         
            //Attach the bow object (her it is shown as cylinder)
            GameObject cylinder = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            cylinder.transform.SetParent(left_hand.transform);
            cylinder.transform.localPosition = new Vector3(0,0.1f,0); 
            cylinder.transform.localRotation = Quaternion.Euler(0,0,90);
            cylinder.transform.localScale = new Vector3(0.1f, 0.5f, 0.1f); 

            //make an anchor object for the top of the bow
            topBox = new GameObject();
            topBox.transform.SetParent(cylinder.transform);
            topBox.transform.localPosition = new Vector3(0,-1f,0f); 
            topBox.transform.localScale = new Vector3(0.2f, 1f, 0.2f);

            //make an anchor object for the bottom of the bow
            bottomBox = new GameObject();
            bottomBox.transform.SetParent(cylinder.transform);
            bottomBox.transform.localPosition = new Vector3(0,1f,0f); 
            bottomBox.transform.localScale = new Vector3(0.2f, 1f, 0.2f);

            //make a line object
            GameObject linePrefab = new GameObject("linePrefab");
            LineRenderer lineRenderer = linePrefab.AddComponent<LineRenderer>();
            lineRenderer.startWidth = 0.01f;
            lineRenderer.endWidth = 0.01f;
            lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
            lineRenderer.startColor = Color.black;
            lineRenderer.endColor = Color.black;

            line = Instantiate(linePrefab).GetComponent<LineRenderer>();
            line.positionCount = 3;
            

            initialized=true;
        }  

        if(!initialized)return;

        //On every frame update the position of the line
        line.SetPosition(0, topBox.transform.position);
        line.SetPosition(1, avatar.getRightHand().transform.position);
        line.SetPosition(2, bottomBox.transform.position);

    }
}
