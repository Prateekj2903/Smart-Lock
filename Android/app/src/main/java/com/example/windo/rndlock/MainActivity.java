package com.example.windo.rndlock;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.FirebaseDatabase;

public class MainActivity extends AppCompatActivity {

    private Button unlockDoorButton;
    private String eMail;
    private FirebaseAuth mAuth;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        unlockDoorButton = (Button) findViewById(R.id.unlock_button);
        mAuth = FirebaseAuth.getInstance();

        eMail = mAuth.getCurrentUser().getEmail();

        Toast.makeText(MainActivity.this, mAuth.getCurrentUser().getEmail(), Toast.LENGTH_LONG).show();

        Log.d("Email", mAuth.getCurrentUser().getEmail());

        unlockDoorButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                FirebaseDatabase.getInstance().getReference().child(eMail.substring(0, eMail.indexOf('@')))
                        .setValue("Unlocked");
            }
        });
    }
}
