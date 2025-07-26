using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Banana : MonoBehaviour
{
    private void OnTriggerEnter2D(Collider2D collision)
    {
        // Debug.Log("Banana touched by: " + collision.name);

        if (collision.CompareTag("Player"))
        {
            BananaCollector.Instance.Collect();
            Destroy(gameObject);
        }
    }
}
