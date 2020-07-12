# youtyper

youtyper is a customizable command-line touch-typing tutor.

You can easily add your customized lesson with text, even Python function.

## Motivation

There're a lot of touch-typing tutor apps.
However, most of the apps doesn't come with the flexibility to maximize my learning rate.

First, the flexibility of lessons.

For example, I'm pretty bad at distinguish "c" and "d", which lies vertically on keyboards, but most of apps provides rowwise lessons.
I'm also not good at typing "y", "u", and "i", but most of apps also includes "o" and "p" in the lessons for these keys.
Some apps provide lessons with custom texts, but which cannot be dynamically generated.
And, I want to create lessons with Python.

Second, the flexibility of analytics.
  
I'm a pretty big fun of keybr.com, because of its beauty and detailed statistics. I may have spent more time watching the graphs than practicing. Though I can't create beautiful interfaces like them, I can provide more detailed statistics and even allow users to analyze their typing.   

## Naming

- "y","o","u","t","p","e",and "r" are all on the upper row of the keyboard
- These keys are why I created this app. 
- This name may also indicates customizability of this app.
 
 ## Install
 ```pip install youtyper```
 
 ## Quickstart
 
```youtyper```: will start a standard lesson with standard analytics enabled.
 
 ## Customize your lessons
Use ```--lesson_type``` to choose your lesson. 

1. Load text to create lessons

    ```youtyper --lesson_type text --text_path path-to-your-lesson-text```
     
    Other options available:
    
    - ```--disable_shuffle```: Disable shuffling of lessons  (default: false)
    - ```--num_lessons 10```: lessons to take (default: None, repeat until exit)
    - ```--len_lessons 50```: Number of maximum characters in a lesson (default: 100)

2. Load python script to enable custome lesson

    ```youtyper --lesson_type python --generator_path path-to-your-lesson-text -- generator_name YourLessonGeneratorClassName```
    
    Use the specified ```LessonGenarator``` class to generate lessons. Example generators are available under ```examples```.
    

3. Load built-in lessons

    ```youtyper --lesson_type built-in --lesson_name right_hand_home_row```
    
    Use the built-in lessons. See lessons/README.md for available lessons. 

## Customize your analyzer

1. Use predefined analyzer

    ```youtyper ... --analyzer cpm error_rate```
    
    - ```cpm```: Character Per Minute
    - ```error_rate```: The ratio of wrong key push
    
    Other options available:
    
    - ```--analyzer wpm```: [To be implemented] Show words per minute
    - ``` --ignore_consecutive_errors```: [To be implemented] Ignore the consecutive error by the same character (deafult: false)

2. Use custome analytics

    ```youtyper ... --analyzer_path path-to-your-kpi-file --analyzer_name YourStatisticsClassName```

    Use the specified ```Analyzer``` class to analyze lesson logs.Example analyzer are available under ```examples```.  
    

## Build your own custom class

1. Custom Lesson

- You must provide a custom ```LessonGenerator``` to create your custom lessons.
    - ```LessonGenarator``` must be a iterator yields ```Lesson```
        - ```LessonGenarator``` must implement ```__len__``` method
        - ```Lesson``` is basically text to type and metadata.
    - Unknown command line options are passed to the ```LessonGenarator``` class as list. 

2. Custom Analytics

- You must provide a custom ```Analyzer``` to create your custom analytics.
    - ```Analyzer``` must generate printable text to show user, and dict to save with lesson.
        - ```Analyzer``` must implement ```analyze``` method which returns ```(Dict, str)```
    - Unknown command line options are passed to the ```LessonGenarator``` class as list. 
        - The prefix is stripped before the option passed to the custom class.
        - You can specify multiple ```Analyzer``` and all the unknown options are passed to all ```Analyzer```.
            - Check your option is not shared by other analyzers unintentionally.
         
## Lesson Log

For further analytics, youtyper saves every lesson log to the ```.youtyper/logs``` under the user's home folder.

A lesson log is a json file named as ```yyyymmdd_hhmmss_[lesson_name]_[lesson_id].json```. 

The structure is as follows:
```json
{
  "lesson_name": "right_hand_home_row",
  "lesson_id": "1",
  "command-line-options": {"lesson_type": "built-in", "lesson_name":"right_hand_home_row"},
  "text": "klj ;l;l;jjk ;ljl; kl;jkl jjlk ljk l; kl ;j",
  "keystrokes": 
  [
    {"timestamp": "2020/07/02 18:00:03", "key":  "k", "target":"l"},
    {"..."}
  ]
  "analytics": 
  {
    "cpm": {"overall": 100.0,"k": 70.6, "l": 116.4,"...": "..."},
    "error_rate": {"overall": 0.043, "k": 0.067,"l": 0.032,"...": "..."},
    "...": "..."
  } 
}
```