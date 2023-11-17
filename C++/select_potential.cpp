#include <iostream>
#include <string>
using namespace std;

string select_potential() {
    cout << "Select a potential to use:" << endl;
    cout << "1. Stillinger-Weber" << endl;
    cout << "2. Axilrod-Teller" << endl;
    
    string choice;
    cout << "Enter the number of your choice: ";
    cin >> choice;

    if (choice == "1") {
        return "Stillinger-Weber";
    } else if (choice == "2") {
        return "Axilrod-Teller";
    } else {
        cerr << "Invalid choice. Exiting." << endl;
        exit(1); // or handle this in a different way
    }
}
