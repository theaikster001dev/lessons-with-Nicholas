using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlySpawner : MonoBehaviour
{

    [Tooltip("Assign fly prefab here")]
    public GameObject flyPrefab;

    [Tooltip("these Transform mark where flies will appear")]
    public Transform[] spawnPoints;

    // Start is called before the first frame update
    void Start()
    {
        if (flyPrefab == null || spawnPoints.Length == 0)
        {
            Debug.LogWarning("FlySpawner needs a refab and at least one spawn point.");
            return;
        }

        foreach (var point in spawnPoints)
        {
            Instantiate(flyPrefab, point.position, Quaternion.identity);
        }

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
