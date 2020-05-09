using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace DataTables
{
    public class SceneRow
    {
	int id;                                           // 主键id 地图id也是场景id
	string comment;                                   // 注释 
	string name;                                      // 名称 场景的名字
	string path;                                      // 场景保存路径 
	int lines;                                        // 分线 0不分线 其他按照配置分线，默认2个分线
	int ismirror;                                     // 场景类型 0不是镜像 1可以是镜像
	int type;                                         // 场景类型 1普通场景 2副本 3镜像
	int server;                                       // 场景所在游戏服 
	
    };

    class SceneTable
    {
        private Dictionary<int, SceneRow> tableDic = new Dictionary<int, SceneRow>();
        private ArrayList tableKeys = new ArrayList();

        const string TABLE_PATH = ".\\";

        private static SceneTable instance = new SceneTable();
        public static SceneTable Instance()
        {
            return instance;
        }

        private string GetJson(string jsonFile)
        {
            using FileStream fsRead = new FileStream(jsonFile, FileMode.Open);
            int fsLen = (int)fsRead.Length;
            byte[] heByte = new byte[fsLen];
            fsRead.Read(heByte, 0, heByte.Length);
            return System.Text.Encoding.UTF8.GetString(heByte);
        }

        public bool GetRow(int key, out SceneRow row)
        {
            return tableDic.TryGetValue(key, out row);
        }

        public bool HasRow(int key)
        {
            return tableDic.ContainsKey(key);
        }

        public ArrayList Keys()
        {
            return tableKeys;
        }

        public Dictionary<int, SceneRow> Table()
        {
            return tableDic;
        }

        public bool Load()
        {
            return LoadJson("Scene.json");
        }

        public bool ReLoad()
        {
            return ReLoadJson("Scene.json");
        }

        private bool LoadJson(string jsonFile)
        {
            try
            {
                string loadFile = TABLE_PATH + jsonFile;
                string json = GetJson(loadFile);
                var tableRows = JsonConvert.DeserializeObject<List<SceneRow>>(json);
                foreach (var row in tableRows)
                {
                    tableDic.Add(row.Id, row);
                    tableKeys.Add(row.Id);
                }
            }
            catch(Exception e)
            {
                Console.WriteLine("{0} First exception.", e.Message);
                return false;
            }
            return true;
        }

        private bool ReLoadJson(string jsonFile)
        {
            tableDic.Clear();
            tableKeys.Clear();
            return LoadJson(jsonFile);
        }
    }
}
