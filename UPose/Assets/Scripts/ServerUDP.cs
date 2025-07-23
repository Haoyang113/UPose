using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using UnityEngine; // 为了使用 Debug.Log

/// <summary>
/// A basic UDP server that listens to a port for incoming data.
/// </summary>
public class ServerUDP
{
    private UdpClient server;
    private IPEndPoint endPoint;
    private bool open;
    private Thread listeningThread;

    private const int BUFFER_SIZE = 1024;
    private byte[] buffer = new byte[BUFFER_SIZE];
    private string latestResponse;

    private readonly string[] eom = new string[] { "<EOM>" };
    private Queue<string> messageBuffer = new Queue<string>();
    private int maxMessageBufferSize;
    private bool suppressWarnings;

    private int port;

    public ServerUDP(string ip, int port, bool suppressWarnings = true, int maximumMessageBufferSize = 100)
    {
        this.port = port;
        this.maxMessageBufferSize = maximumMessageBufferSize;
        this.suppressWarnings = suppressWarnings;
        // UdpClient 会在 StartListeningAsync 中创建，以避免在主线程上构造时出现问题
    }

    public void Connect()
    {
        if (open) return;
        open = true;
        StartListeningAsync();
    }

    public void Disconnect()
    {
        open = false;
        // 关闭 server 会让正在阻塞的 Receive() 方法抛出异常，从而使线程自然退出
        if (server != null)
        {
            server.Close();
            server = null;
        }

        if (listeningThread != null && listeningThread.IsAlive)
        {
            listeningThread.Join(); // 等待线程结束
        }
    }

    private void StartListeningAsync()
    {
        // 如果线程已在运行，则先停止
        if (listeningThread != null && listeningThread.IsAlive)
        {
            Disconnect();
        }
        
        listeningThread = new Thread(new ThreadStart(StartListening));
        listeningThread.IsBackground = true; // 设置为后台线程，以便在主程序退出时自动关闭
        listeningThread.Start();
    }

    private void StartListening()
    {
        try
        {
            server = new UdpClient(port, AddressFamily.InterNetwork);
            endPoint = new IPEndPoint(IPAddress.Any, port);
        }
        catch (Exception e)
        {
            Debug.LogError($"[ServerUDP] Failed to create UdpClient on port {port}: {e.Message}");
            return;
        }
        
        Debug.Log($"[ServerUDP] Waiting for messages @Port: {port}");
        messageBuffer.Clear();

        while (open)
        {
            try
            {
                buffer = server.Receive(ref endPoint);
                if (buffer.Length > 0)
                {
                    latestResponse = Encoding.UTF8.GetString(buffer, 0, buffer.Length);
                    string[] sa = latestResponse.Split(eom, StringSplitOptions.None);
                    for (int i = 0; i < sa.Length - 1; ++i)
                    {
                        // 在Unity主线程外操作队列需要加锁，但此处为单生产者-单消费者，且都由我们控制，暂时简化
                        if (messageBuffer.Count >= maxMessageBufferSize)
                        {
                            messageBuffer.Dequeue();
                            if (!suppressWarnings)
                                Debug.LogWarning("[ServerUDP] Message queue full, dropping oldest message.");
                        }
                        messageBuffer.Enqueue(sa[i]);
                    }
                }
            }
            catch (SocketException ex)
            {
                // 当调用 server.Close() 时，也会触发一个异常，这是正常关闭线程的方式
                if (open) // 只有在意外情况下才打印错误
                {
                    Debug.LogError($"[ServerUDP] SocketException: {ex.Message}");
                }
                // 不再进行递归调用，直接退出循环
                break; 
            }
            catch (Exception ex)
            {
                Debug.LogError($"[ServerUDP] An unexpected error occurred: {ex.ToString()}");
                break; // 发生任何其他错误时也退出循环
            }
        }
        
        Debug.Log("[ServerUDP] Listening thread finished.");
    }

    public bool HasMessage()
    {
        return messageBuffer.Count > 0;
    }

    public string GetMessage()
    {
        if (messageBuffer.Count > 0)
        {
            return messageBuffer.Dequeue();
        }
        return null;
    }
}