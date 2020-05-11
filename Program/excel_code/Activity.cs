using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace DataTables
{
    public class ActivityRow
    {
	int id;                                           // ����id �id
	string comment;                                   // ע�� 
	int tab_id;                                       // ��ǩ��� �������ǩ
	int weight;                                       // Ȩ�� ��ǩ�б��ڵ���ʾȨ��
	int name_id;                                      // ����id �����id
	int describe_id;                                  // �����ı�id 
	int race_id;                                      // �Ƿ�������� �Ƿ���Ҫ�ж������������ʾ�Ի���ť,0��ʾ��1��ʾ��
	string main_icon;                                 // ��ͼ���� 
	string sub_icon;                                  // ��ͼ���� 
	int function_on;                                  // �Ƿ��� 0 ������ 1 ����
	int recommend;                                    // �Ƿ����Ƽ� 0 ������ 1 ����
	int call;                                         // ֧�ֿ����������� 0 ������ 1 ����
	int push;                                         // ֧�ֿ����������� 0 ������ 1 ����
	int open_type;                                    // ʱ������ 1 ȫ�쿪�� 2 ��ʱ����
	List<int> open_in_week;                           // �����ܴ� ��ʱ����ʱʹ�� ������2|4
	List<int> open_in_day;                            // ����ʱ�� ��ʱ����ʱʹ�� ���� 00:00 - 23:59�� 0|0|23|59
	int reset_type;                                   // ���ô������� 1 ÿ�� 2 ÿ��
	int level_min;                                    // ��͵ȼ����� 
	int player_min;                                   // ������������� 
	int active_value;                                 // ��Ծ�Ƚ��� ���ÿ���������Ļ�Ծ��
	int rounds_max;                                   // �ִ������� 
	int times_max;                                    // ���������� ��=������
	List<int> drop_rounds;                            // ÿ�ֵ��佱�� ���㷽ʽ|�����id ��������㣺0���ʣ�1Ȩֵ��
	List<int> drop_times;                             // ÿ�����佱�� ���㷽ʽ|�����id ��������㣺0���ʣ�1Ȩֵ��
	List<int> drop_display;                           // ������ʾ 
	List<int> scene_id;                               // ����id ��漰�����г���id
	int quest_id;                                     // ��¼����id ��¼��Ծ�ȵ�����id
	
    };

    class ActivityTable
    {
        private Dictionary<int, ActivityRow> tableDic = new Dictionary<int, ActivityRow>();
        private ArrayList tableKeys = new ArrayList();

        const string TABLE_PATH = ".\\";

        private static ActivityTable instance = new ActivityTable();
        public static ActivityTable Instance()
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

        public bool GetRow(int key, out ActivityRow row)
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

        public Dictionary<int, ActivityRow> Table()
        {
            return tableDic;
        }

        public bool Load()
        {
            return LoadJson("Activity.json");
        }

        public bool ReLoad()
        {
            return ReLoadJson("Activity.json");
        }

        private bool LoadJson(string jsonFile)
        {
            try
            {
                string loadFile = TABLE_PATH + jsonFile;
                string json = GetJson(loadFile);
                var tableRows = JsonConvert.DeserializeObject<List<ActivityRow>>(json);
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
