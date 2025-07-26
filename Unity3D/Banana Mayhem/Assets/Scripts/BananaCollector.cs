using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BananaCollector : MonoBehaviour
{
    public static BananaCollector Instance;
    public int score = 0;
    public Text scoreText;

    void Awake()
    {
        if (Instance == null)
            Instance = this;
    }

    public void Collect()
    {
        score++;
        Debug.Log("Score Updated: " + score);

        if (scoreText != null)
        {
            scoreText.text = "Bananas: " + score;
        }
        else
        {
            Debug.LogWarning("ScoreText is NULL!");
        }
    }
}