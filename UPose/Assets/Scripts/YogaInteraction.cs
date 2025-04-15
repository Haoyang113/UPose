using UnityEngine;

public class YogaInteraction : MonoBehaviour
{
    ReadyPlayerAvatar avatar;
    bool initialized = false;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        avatar = GetComponent<ReadyPlayerAvatar>();
    }

    bool above40 = false;
    int counter = 0;

    // Update is called once per frame
    void Update()
    {
        if (!initialized && avatar.isLoaded())
        {
            //Do any initial things to the avatar here...


            initialized = true;
        }
        if (!initialized) return;
        //After this line you can assume that the avatar is loaded


        Quaternion rotation = avatar.getRightHipRotation();
        float AngleX = Mathf.Abs(rotation.eulerAngles.z);

        //Debug.Log(AngleX);
        if (above40==false && AngleX > 210)
        {
            above40 = true;
            counter++;
            Debug.Log(counter);
            //Display this on a texture
        }
        else if(above40==true && AngleX < 190)
        {
            above40 = false;
        }
        

    }
}
