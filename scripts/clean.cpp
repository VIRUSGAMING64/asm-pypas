#include <bits/stdc++.h>
#include <string>
#include <filesystem>

using namespace std;
filesystem::path base = ".";

string getname(string a) 
{
    int n = a.size()-1;
    string ns = "";
    while(a[n] != '/'){
        ns = a[n] + ns;
        n--;
    }
    return ns;
}

bool in(string a, string b)
{
    if (b.size() > a.size())return false;
    for(int i = 0; i < a.size(); i++)
    {
        if (i + b.size() <= a.size())
        {
            bool ok = true;
            for (int j = 0; (j < b.size()); j++)
            {
                if (a[i + j] != b[j])
                {
                    ok = false;
                    break;
                }
            }
            if(ok)
            {
                return true;
            }
        }
    }
    return false;
}

int main() 
{
    base = filesystem::current_path();
    cout << "current path:  " << base << endl << "removeds: \n";
    queue<filesystem::path> q ;
    vector<string> erase;

    ifstream cl(".clean");
    while(!cl.eof())
    {
        string a;
        cl >> a;
        erase.push_back(a);
    }

    q.push(base);
    while(!q.empty())
    {
        filesystem::path curr = q.front();
        q.pop();

        for(auto entry : filesystem::directory_iterator(curr))
        {
            bool ok = false;
            string n_entry = getname(entry.path().string());
            for(auto c : erase)
            {
                if (in(n_entry, c))
                {
                    ok = true;
                    filesystem::remove_all(entry);
                    cout << entry << endl;
                }
            }
            if(!ok && filesystem::is_directory(entry))
            {
                q.push(entry);
            }
        }

    }
    

}