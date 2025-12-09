#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Student {
    string id;
    string name;
    int age;
    string grade;
    string major;
    
    // Constructor with default values
    Student() : id(""), name(""), age(0), grade(""), major("") {}
};

// Function to trim whitespace
string trim(const string& str) {
    size_t first = str.find_first_not_of(" \t\n\r\"");
    if (first == string::npos) return "";
    size_t last = str.find_last_not_of(" \t\n\r\"");
    return str.substr(first, (last - first + 1));
}

// Parse JSON manually
vector<Student> parseJSON(const string& filename) {
    vector<Student> students;
    ifstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error: Could not open " << filename << endl;
        return students;
    }
    
    string line;
    Student current;
    bool inObject = false;
    
    while (getline(file, line)) {
        line = trim(line);
        
        if (line == "{") {
            inObject = true;
            current = Student();
        }
        else if (line == "}" || line == "},") {
            if (inObject && !current.id.empty()) {
                students.push_back(current);
                inObject = false;
            }
        }
        else if (inObject) {
            size_t colonPos = line.find(":");
            if (colonPos != string::npos) {
                string key = trim(line.substr(0, colonPos));
                string value = trim(line.substr(colonPos + 1));
                
                // Remove trailing comma
                if (!value.empty() && value.back() == ',') {
                    value = value.substr(0, value.length() - 1);
                }
                value = trim(value);
                
                if (key == "\"id\"") {
                    current.id = value;
                }
                else if (key == "\"name\"") {
                    current.name = value;
                }
                else if (key == "\"age\"") {
                    try {
                        current.age = stoi(value);
                    } catch (const exception& e) {
                        cerr << "Warning: Invalid age value for student. Using 0." << endl;
                        current.age = 0;
                    }
                }
                else if (key == "\"grade\"") {
                    current.grade = value;
                }
                else if (key == "\"major\"") {
                    current.major = value;
                }
            }
        }
    }
    
    file.close();
    return students;
}

// Sort students by age (for output)
vector<Student> sortByAge(vector<Student> students) {
    sort(students.begin(), students.end(), 
         [](const Student& a, const Student& b) {
             return a.age < b.age;
         });
    return students;
}

// Display student list
void displayStudents(const vector<Student>& students) {
    if (students.empty()) {
        cout << "No students found in the database!" << endl;
        return;
    }
    
    cout << "========================================" << endl;
    cout << "      STUDENT RECORDS REPORT" << endl;
    cout << "========================================" << endl << endl;
    
    cout << "Total Students: " << students.size() << endl << endl;
    
    cout << left << setw(15) << "ID" 
         << setw(25) << "Name" 
         << setw(8) << "Age" 
         << setw(10) << "Grade" 
         << setw(20) << "Major" << endl;
    cout << string(78, '-') << endl;
    
    for (const auto& student : students) {
        cout << left << setw(15) << trim(student.id)
             << setw(25) << trim(student.name)
             << setw(8) << student.age
             << setw(10) << trim(student.grade)
             << setw(20) << trim(student.major) << endl;
    }
    
    cout << endl;
    cout << "========================================" << endl;
    cout << "  Report generated successfully!" << endl;
    cout << "========================================" << endl;
}

// Save detailed report to file
void saveDetailedReport(const vector<Student>& students, const string& filename) {
    ofstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error: Could not create report file!" << endl;
        return;
    }
    
    file << "DETAILED STUDENT REPORT" << endl;
    file << "==============================================" << endl << endl;
    
    vector<Student> sortedStudents = sortByAge(students);
    
    file << "Total Students: " << students.size() << endl << endl;
    
    file << left << setw(15) << "ID" 
         << setw(25) << "Name" 
         << setw(8) << "Age" 
         << setw(10) << "Grade" 
         << setw(20) << "Major" << endl;
    file << string(78, '-') << endl;
    
    for (const auto& student : sortedStudents) {
        file << left << setw(15) << trim(student.id)
             << setw(25) << trim(student.name)
             << setw(8) << student.age
             << setw(10) << trim(student.grade)
             << setw(20) << trim(student.major) << endl;
    }
    
    file.close();
    cout << "\nDetailed report saved to: " << filename << endl;
}

int main() {
    // Read students from JSON file
    vector<Student> students = parseJSON("students.json");
    
    if (students.empty()) {
        cout << "No students found or error reading file!" << endl;
        return 1;
    }
    
    // Display students
    displayStudents(students);
    
    // Save detailed report
    saveDetailedReport(students, "student_report.txt");
    
    return 0;
}
