using UnityEngine;

public interface MotionTrackingPose
{
    public Quaternion GetRotation(Landmark i);
    public long getFrameCounter();
}
