using UnityEngine;

public class WaterGenerator : MonoBehaviour
{
    [Header("设置生成内容")]
    public GameObject ballPrefab;      // 小球预制体
    public Transform spawnPoint;       // 生成位置
    public float spawnInterval = 1f;   // 生成时间间隔

    [Header("小球初始参数")]
    public Vector3 initialVelocity = Vector3.zero;

    private float timer;

    void Update()
    {
        if (ballPrefab == null || spawnPoint == null) return;

        timer += Time.deltaTime;

        if (timer >= spawnInterval)
        {
            SpawnBall();
            timer = 0f;
        }
    }

    void SpawnBall()
    {
        GameObject newBall = Instantiate(ballPrefab, spawnPoint.position, Quaternion.identity,transform);
        Rigidbody rb = newBall.GetComponent<Rigidbody>();
        if (rb != null)
        {
            rb.velocity = initialVelocity;
        }
    }
}
