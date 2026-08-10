#!/usr/bin/env python3
"""
AI Code Extractor Project Generator
Run this script once to generate all project files in proper structure
Usage: python3 generate_project.py
"""

import os

# Base project structure
PROJECT_NAME = "AICodeExtractor"
BASE_PATH = os.path.expanduser(f"~/storage/downloads/{PROJECT_NAME}")

# All file contents - THE COMPLETE PROJECT
FILES = {
    # Java Source Files
    "app/src/main/java/com/codeextractor/service/CodeExtractorAccessibilityService.java": '''package com.codeextractor.service;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.util.Log;
import java.util.List;
import java.util.ArrayList;

public class CodeExtractorAccessibilityService extends AccessibilityService {
    
    private static final String TAG = "CodeExtractor";
    private CodeProcessor processor;
    
    @Override
    public void onServiceConnected() {
        processor = new CodeProcessor(this);
        
        AccessibilityServiceInfo info = new AccessibilityServiceInfo();
        info.eventTypes = AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED | 
                         AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED;
        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC;
        info.flags = AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS |
                    AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS;
        info.notificationTimeout = 100;
        
        setServiceInfo(info);
        Log.d(TAG, "Accessibility Service Connected");
    }
    
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        String packageName = event.getPackageName() != null ? 
                           event.getPackageName().toString() : "";
        
        if (isAIChatApp(packageName)) {
            AccessibilityNodeInfo rootNode = getRootInActiveWindow();
            if (rootNode != null) {
                extractTextContent(rootNode, packageName);
                rootNode.recycle();
            }
        }
    }
    
    private boolean isAIChatApp(String packageName) {
        return packageName.contains("openai") ||
               packageName.contains("anthropic") ||
               packageName.contains("claude") ||
               packageName.contains("chatgpt") ||
               packageName.contains("bard") ||
               packageName.contains("gemini") ||
               packageName.contains("copilot") ||
               packageName.contains("chrome") ||
               packageName.contains("firefox") ||
               packageName.contains("browser");
    }
    
    private void extractTextContent(AccessibilityNodeInfo node, String source) {
        if (node == null) return;
        
        CharSequence text = node.getText();
        if (text != null && text.length() > 0) {
            processor.processText(text.toString(), source);
        }
        
        int childCount = node.getChildCount();
        for (int i = 0; i < childCount; i++) {
            AccessibilityNodeInfo child = node.getChild(i);
            if (child != null) {
                extractTextContent(child, source);
                child.recycle();
            }
        }
    }
    
    @Override
    public void onInterrupt() {
        Log.d(TAG, "Service Interrupted");
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        if (processor != null) {
            processor.cleanup();
        }
    }
}''',

    "app/src/main/java/com/codeextractor/service/CodeProcessor.java": '''package com.codeextractor.service;

import android.content.Context;
import android.util.Log;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.HashMap;
import java.util.Map;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class CodeProcessor {
    
    private static final String TAG = "CodeProcessor";
    private Context context;
    private Map<String, StringBuilder> conversationBuffers;
    private Map<String, StringBuilder> codeBuffers;
    
    private static final Pattern CODE_BLOCK_PATTERN = Pattern.compile(
        "```[\\\\w]*\\\\n([\\\\s\\\\S]*?)```|`([^`]+)`|(?m)^(?:[ ]{4}|\\\\t)(.+)$"
    );
    
    private static final Map<String, Pattern> LANGUAGE_PATTERNS = new HashMap<>();
    static {
        LANGUAGE_PATTERNS.put("python", Pattern.compile("\\\\b(def|import|class|if __name__|print|return)\\\\b"));
        LANGUAGE_PATTERNS.put("javascript", Pattern.compile("\\\\b(function|const|let|var|=>|console\\\\.log)\\\\b"));
        LANGUAGE_PATTERNS.put("java", Pattern.compile("\\\\b(public|private|class|void|static|new)\\\\b"));
        LANGUAGE_PATTERNS.put("cpp", Pattern.compile("\\\\b(#include|std::|cout|cin|namespace)\\\\b"));
        LANGUAGE_PATTERNS.put("sql", Pattern.compile("\\\\b(SELECT|FROM|WHERE|INSERT|UPDATE|DELETE)\\\\b", Pattern.CASE_INSENSITIVE));
    }
    
    public CodeProcessor(Context context) {
        this.context = context;
        this.conversationBuffers = new HashMap<>();
        this.codeBuffers = new HashMap<>();
    }
    
    public void processText(String text, String source) {
        if (text == null || text.trim().isEmpty()) return;
        
        if (!conversationBuffers.containsKey(source)) {
            conversationBuffers.put(source, new StringBuilder());
            codeBuffers.put(source, new StringBuilder());
        }
        
        Matcher codeMatcher = CODE_BLOCK_PATTERN.matcher(text);
        boolean hasCode = false;
        
        while (codeMatcher.find()) {
            String codeSnippet = codeMatcher.group(1);
            if (codeSnippet == null) codeSnippet = codeMatcher.group(2);
            if (codeSnippet == null) codeSnippet = codeMatcher.group(3);
            
            if (codeSnippet != null && !codeSnippet.trim().isEmpty()) {
                hasCode = true;
                String language = detectLanguage(codeSnippet);
                saveCode(codeSnippet, language, source);
            }
        }
        
        if (!hasCode || text.length() > 100) {
            String cleanText = codeMatcher.replaceAll("[CODE]");
            conversationBuffers.get(source).append(cleanText).append("\\n");
            
            if (conversationBuffers.get(source).length() > 5000) {
                saveConversation(source);
            }
        }
    }
    
    private String detectLanguage(String code) {
        Map<String, Integer> scores = new HashMap<>();
        
        for (Map.Entry<String, Pattern> entry : LANGUAGE_PATTERNS.entrySet()) {
            Matcher matcher = entry.getValue().matcher(code);
            int count = 0;
            while (matcher.find()) count++;
            if (count > 0) scores.put(entry.getKey(), count);
        }
        
        String detectedLang = "unknown";
        int maxScore = 0;
        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            if (entry.getValue() > maxScore) {
                maxScore = entry.getValue();
                detectedLang = entry.getKey();
            }
        }
        return detectedLang;
    }
    
    private void saveCode(String code, String language, String source) {
        try {
            File baseDir = new File(context.getExternalFilesDir(null), "AICodeExtractor");
            File langDir = new File(baseDir, language);
            if (!langDir.exists()) langDir.mkdirs();
            
            String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
            String filename = source.replaceAll("[^a-zA-Z0-9]", "_") + "_" + timestamp + "." + getExtension(language);
            
            File codeFile = new File(langDir, filename);
            FileWriter writer = new FileWriter(codeFile, true);
            writer.write(code + "\\n\\n");
            writer.close();
            
            Log.d(TAG, "Saved: " + codeFile.getAbsolutePath());
        } catch (IOException e) {
            Log.e(TAG, "Error saving code", e);
        }
    }
    
    private void saveConversation(String source) {
        try {
            File baseDir = new File(context.getExternalFilesDir(null), "AICodeExtractor/conversations");
            if (!baseDir.exists()) baseDir.mkdirs();
            
            String date = new SimpleDateFormat("yyyyMMdd", Locale.US).format(new Date());
            String filename = source.replaceAll("[^a-zA-Z0-9]", "_") + "_" + date + ".txt";
            
            FileWriter writer = new FileWriter(new File(baseDir, filename), true);
            writer.write(conversationBuffers.get(source).toString());
            writer.close();
            
            conversationBuffers.get(source).setLength(0);
        } catch (IOException e) {
            Log.e(TAG, "Error saving conversation", e);
        }
    }
    
    private String getExtension(String language) {
        switch (language) {
            case "python": return "py";
            case "javascript": return "js";
            case "java": return "java";
            case "cpp": return "cpp";
            case "sql": return "sql";
            default: return "txt";
        }
    }
    
    public void cleanup() {
        for (String source : conversationBuffers.keySet()) {
            if (conversationBuffers.get(source).length() > 0) {
                saveConversation(source);
            }
        }
    }
}''',

    "app/src/main/java/com/codeextractor/service/VoiceInterfaceService.java": '''package com.codeextractor.service;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.speech.tts.TextToSpeech;
import android.speech.SpeechRecognizer;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.os.Bundle;
import android.util.Log;
import java.util.ArrayList;
import java.util.Locale;
import java.util.regex.Pattern;

public class VoiceInterfaceService extends Service implements TextToSpeech.OnInitListener {
    
    private static final String TAG = "VoiceInterface";
    private TextToSpeech tts;
    private SpeechRecognizer speechRecognizer;
    private boolean isTTSReady = false;
    
    private static final Pattern CODE_FILTER = Pattern.compile("```[\\\\s\\\\S]*?```|`[^`]+`");
    
    @Override
    public void onCreate() {
        super.onCreate();
        tts = new TextToSpeech(this, this);
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        setupRecognitionListener();
    }
    
    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            tts.setLanguage(Locale.US);
            tts.setSpeechRate(0.9f);
            isTTSReady = true;
            Log.d(TAG, "TTS Ready");
        }
    }
    
    private void setupRecognitionListener() {
        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override public void onReadyForSpeech(Bundle params) {}
            @Override public void onBeginningOfSpeech() {}
            @Override public void onRmsChanged(float rmsdB) {}
            @Override public void onBufferReceived(byte[] buffer) {}
            @Override public void onEndOfSpeech() {}
            @Override public void onError(int error) { Log.e(TAG, "Speech error: " + error); }
            
            @Override
            public void onResults(Bundle results) {
                ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if (matches != null && !matches.isEmpty()) {
                    Intent broadcast = new Intent("com.codeextractor.SPOKEN_INPUT");
                    broadcast.putExtra("text", matches.get(0));
                    sendBroadcast(broadcast);
                }
            }
            
            @Override public void onPartialResults(Bundle partialResults) {}
            @Override public void onEvent(int eventType, Bundle params) {}
        });
    }
    
    public void speakText(String text) {
        if (!isTTSReady) return;
        String cleanText = CODE_FILTER.matcher(text).replaceAll("[code omitted]").trim();
        if (!cleanText.isEmpty()) {
            tts.speak(cleanText, TextToSpeech.QUEUE_ADD, null, null);
        }
    }
    
    public void startListening() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        speechRecognizer.startListening(intent);
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    @Override
    public void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        if (speechRecognizer != null) {
            speechRecognizer.destroy();
        }
        super.onDestroy();
    }
}''',

    "app/src/main/java/com/codeextractor/widget/CodeExtractorWidget.java": '''package com.codeextractor.widget;

import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.widget.RemoteViews;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.SharedPreferences;
import com.codeextractor.R;

public class CodeExtractorWidget extends AppWidgetProvider {
    
    private static final String ACTION_VOICE = "VOICE";
    private static final String ACTION_TTS = "TTS";
    
    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) {
            RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.widget_layout);
            
            SharedPreferences prefs = context.getSharedPreferences("Stats", Context.MODE_PRIVATE);
            views.setTextViewText(R.id.code_count, String.valueOf(prefs.getInt("code_count", 0)));
            views.setTextViewText(R.id.language_count, String.valueOf(prefs.getInt("language_count", 0)));
            views.setTextViewText(R.id.file_count, String.valueOf(prefs.getInt("file_count", 0)));
            
            Intent voiceIntent = new Intent(context, CodeExtractorWidget.class);
            voiceIntent.setAction(ACTION_VOICE);
            PendingIntent voicePending = PendingIntent.getBroadcast(context, 0, voiceIntent, 
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            views.setOnClickPendingIntent(R.id.voice_input_button, voicePending);
            
            appWidgetManager.updateAppWidget(appWidgetId, views);
        }
    }
    
    @Override
    public void onReceive(Context context, Intent intent) {
        super.onReceive(context, intent);
        if (ACTION_VOICE.equals(intent.getAction())) {
            Intent voiceService = new Intent(context, com.codeextractor.service.VoiceInterfaceService.class);
            context.startService(voiceService);
        }
    }
}''',

    "app/src/main/java/com/codeextractor/MainActivity.java": '''package com.codeextractor;

import android.os.Bundle;
import android.content.Intent;
import android.provider.Settings;
import androidx.appcompat.app.AppCompatActivity;
import android.widget.TextView;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        Button enableButton = findViewById(R.id.enable_button);
        enableButton.setOnClickListener(v -> {
            startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS));
        });
    }
}''',

    # XML Resources
    "app/src/main/res/layout/widget_layout.xml": '''<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp"
    android:background="#2C3352">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="20dp">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="AI Code Extractor"
            android:textSize="18sp"
            android:textColor="#E8EAF0"
            android:paddingBottom="16dp"/>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal">

            <LinearLayout
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:orientation="vertical"
                android:gravity="center">

                <TextView
                    android:id="@+id/code_count"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="0"
                    android:textSize="24sp"
                    android:textColor="#4ECDC4"/>

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Code Blocks"
                    android:textSize="12sp"
                    android:textColor="#A8B2C8"/>
            </LinearLayout>

            <LinearLayout
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:orientation="vertical"
                android:gravity="center">

                <TextView
                    android:id="@+id/language_count"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="0"
                    android:textSize="24sp"
                    android:textColor="#9B72CB"/>

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Languages"
                    android:textSize="12sp"
                    android:textColor="#A8B2C8"/>
            </LinearLayout>

            <LinearLayout
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:orientation="vertical"
                android:gravity="center">

                <TextView
                    android:id="@+id/file_count"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="0"
                    android:textSize="24sp"
                    android:textColor="#5EA3D0"/>

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Files"
                    android:textSize="12sp"
                    android:textColor="#A8B2C8"/>
            </LinearLayout>
        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:gravity="center"
            android:paddingTop="16dp">

            <Button
                android:id="@+id/voice_input_button"
                android:layout_width="56dp"
                android:layout_height="56dp"
                android:text="🎤"
                android:textSize="24sp"
                android:background="#4ECDC4"
                android:layout_marginEnd="16dp"/>

            <Button
                android:id="@+id/tts_button"
                android:layout_width="56dp"
                android:layout_height="56dp"
                android:text="▶"
                android:textSize="24sp"
                android:background="#9B72CB"
                android:layout_marginStart="16dp"/>
        </LinearLayout>

    </LinearLayout>

</RelativeLayout>''',

    "app/src/main/res/layout/activity_main.xml": '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    android:gravity="center">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="AI Code Extractor"
        android:textSize="24sp"
        android:paddingBottom="32dp"/>

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Enable accessibility service to start extracting code"
        android:textSize="16sp"
        android:gravity="center"
        android:paddingBottom="16dp"/>

    <Button
        android:id="@+id/enable_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Enable Service"
        android:textSize="16sp"/>

</LinearLayout>''',

    "app/src/main/res/values/colors.xml": '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="background_primary">#1A1D2E</color>
    <color name="background_card">#2C3352</color>
    <color name="accent_teal">#4ECDC4</color>
    <color name="accent_purple">#9B72CB</color>
    <color name="accent_blue">#5EA3D0</color>
    <color name="text_primary">#E8EAF0</color>
    <color name="text_secondary">#A8B2C8</color>
</resources>''',

    "app/src/main/res/values/strings.xml": '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">AI Code Extractor</string>
    <string name="widget_description">Extract code from AI chats automatically</string>
    <string name="accessibility_service_description">Monitors AI chat apps to extract and organize code snippets</string>
</resources>''',

    "app/src/main/res/xml/accessibility_service_config.xml": '''<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeViewTextChanged|typeWindowContentChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagReportViewIds|flagRetrieveInteractiveWindows"
    android:canRetrieveWindowContent="true"
    android:description="@string/accessibility_service_description"
    android:notificationTimeout="100"/>''',

    "app/src/main/res/xml/widget_info.xml": '''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:minWidth="320dp"
    android:minHeight="200dp"
    android:updatePeriodMillis="1800000"
    android:initialLayout="@layout/widget_layout"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen"
    android:description="@string/widget_description"/>''',

    "app/src/main/AndroidManifest.xml": '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.codeextractor">

    <uses-permission android:name="android.permission.RECORD_AUDIO"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:supportsRtl="true">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <service
            android:name=".service.CodeExtractorAccessibilityService"
            android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.accessibilityservice.AccessibilityService"/>
            </intent-filter>
            <meta-data
                android:name="android.accessibilityservice"
                android:resource="@xml/accessibility_service_config"/>
        </service>

        <service
            android:name=".service.VoiceInterfaceService"
            android:exported="false"/>

        <receiver
            android:name=".widget.CodeExtractorWidget"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE"/>
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/widget_info"/>
        </receiver>

    </application>

</manifest>''',

    "app/build.gradle": '''plugins {
    id 'com.android.application'
}

android {
    namespace 'com.codeextractor'
    compileSdk 34

    defaultConfig {
        applicationId "com.codeextractor"
        minSdk 26
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
}''',

    "settings.gradle": '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "AICodeExtractor"
include ':app' ''',

    "README.md": '''# AI Code Extractor

Automatically extracts code from AI chat sessions on Android.

## Features
- Monitors multiple AI chats simultaneously
- Auto-detects programming languages
- GitHub-style folder organization
- Voice input/output
- Beautiful widget interface

## Setup
1. Import into Android Studio
2. Build and install
3. Enable accessibility service
4. Add widget to home screen

## Usage
Just chat with your AI assistants - code is automatically extracted and organized!

Files saved to: /storage/emulated/0/Android/data/com.codeextractor/files/AICodeExtractor/
'''
}

def create_project_structure():
    """Generate all project files"""
    print("=" * 60)
    print("AI CODE EXTRACTOR - PROJECT GENERATOR")
    print("=" * 60)
    print(f"\\nCreating project in: {BASE_PATH}\\n")
    
    # Create base directory
    os.makedirs(BASE_PATH, exist_ok=True)
    
    # Generate all files
    file_count = 0
    for filepath, content in FILES.items():
        full_path = os.path.join(BASE_PATH, filepath)
        
        # Create directory structure
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        file_count += 1
        print(f"✓ {filepath}")
    
    print(f"\\n{'=' * 60}")
    print(f"✅ SUCCESS! Created {file_count} files")
    print(f"{'=' * 60}")
    print(f"\\n📁 Location: {BASE_PATH}")
    print("\\n📋 Next Steps:")
    print("   1. Transfer folder to your computer")
    print("   2. Open in Android Studio")
    print("   3. Build & install on device")
    print("   4. Enable accessibility service")
    print("   5. Add widget to home screen")
    print("\\n🚀 Then just chat with AIs - code auto-extracts!")

if __name__ == "__main__":
    try:
        create_project_structure()
    except Exception as e:
        print(f"\\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()