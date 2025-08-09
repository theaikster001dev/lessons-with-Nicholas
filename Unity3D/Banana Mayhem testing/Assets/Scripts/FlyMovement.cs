using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class FlyMovement : MonoBehaviour
{

    [Tooltip("Chase speed in unbita per second")]
    public float speed = 3f;

    private Transform player;

    // Start is called before the first frame update
    void Start()
    {
        var playerGO = GameObject.FindWithTag("Player");
        if (playerGO != null)
            player = playerGO.transform;
        else
            Debug.LogError("No GameObject with tag 'Player' found in scene.");

    }

    // Update is called once per frame
    void Update()
    {
        if (player == null) return;

        Vector2 direction = (player.position - transform.position).normalized;

        transform.Translate(direction * speed * Time.deltaTime);
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }
    }
}
