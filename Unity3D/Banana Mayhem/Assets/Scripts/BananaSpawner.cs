using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BananaSpawner : MonoBehaviour
{
    public GameObject bananaPrefab;
    public Transform[] spawnPoints;

    void Start()
    {
        foreach (var point in spawnPoints)
        {
            Instantiate(bananaPrefab, point.position, Quaternion.identity);
        }
    }
}
