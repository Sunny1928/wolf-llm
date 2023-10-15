class Prompts:
    def __init__(self, player_id, room_setting, user_role):

        self.player_id = player_id
        self.room_setting = room_setting
        self.user_role = user_role
        self.info = [
            '我救0號玩家，因為現在還不知道其他玩家的身份，不排除0號玩家是平民或神職，所以為了增加神職陣營的存活機會，我會使用解藥（只有5號玩家看的到此資訊）',
            '第一天晚上是平安夜',
            '1號玩家發言: 我是預言家，0號是狼人，女巫毒藥可以先留著，出完0號後輪次是領先的。',
            '2號玩家發言: 看後面有沒有人跳預言家，沒有的話我會先信1號玩家。',
            '3號玩家發言: 我才是預言家 我查1號是狼 小心他自刀 注意等一下要保他的人',
            '4號玩家發言: 剛剛1號玩家想滿久的才打，3號玩家打很快也可能是單純反應很快，在猶豫該相信誰還是棄票',
            '5號玩家發言: 我是好人，我原本想要歸成平票，但是這樣一定會死人，四號玩家有想要棄票所以我暫時會選擇相信他，小心一二雙狼，我會先票一號玩家。'
        ]
        self.guess_roles = []
        self.alive = [0, 1, 2, 3, 4, 5] # alive players
        self.teammate = []
        
        self.stage_detail={
            "guess-role":{
                "stage_description":"猜測玩家角色階段，你要藉由你有的資訊猜測玩家角色",
                "prompt":f'根據以上綜合資訊，請你判斷所有{self.alive}號玩家最符合的角色及你認為正確的機率百分比(直接回答"[玩家]號玩家: [角色]，[正確的機率百分比]，[原因]"，不需要其他廢話，回答完直接結束回答)'
            },
            "werewolf-dialogue":{
                "stage_description":"狼人發言階段，狼人發言階段，狼人和其他狼人發言",
                "prompt":
                f'''
                根據以上綜合資訊，你有三個選項，請選擇其中一個選項當作發言？
                1. 我同意隊友的發言。請在{self.teammate}號玩家中，選擇一位隊友(若選擇此選項，請直接回答"選項1，[玩家]號玩家：[原因]"，不需要其他廢話，回答完直接結束回答)
                2. 想殺某位玩家，並猜測玩家的角色。從{self.alive}中，選擇一位想殺的玩家，且從預言家和女巫{"和獵人" if self.room_setting["hunter"] else ""}中選一位你認為是此玩家的角色(若選擇此選項，請直接回答"選項2，[玩家]號玩家，[角色]：[原因]"，不需要其他廢話，回答完直接結束回答)
                3. 無發言(若選擇此選項，請直接回答"選項3：[原因]"，不需要其他廢話，回答完直接結束回答)
                '''
            },
            "werewolf":{
                "stage_description":"狼人殺人階段，狼人可以殺一位玩家",
                "prompt":f'根據以上綜合資訊，請從{self.alive}號玩家中，選擇一位要殺的玩家並簡述原因？(直接回答"[玩家]號玩家，[原因]"，不需要其他廢話，回答完直接結束回答)'
            },
            "seer":{
                "stage_description":"猜測玩家角色階段，預言家可以查驗其他玩家的身份",
                "prompt":f'根據以上綜合資訊，請問你要從{self.alive}號玩家中，查驗哪一位玩家並簡述原因？(直接回答"[玩家]號玩家，[原因]"，不需要其他廢話，回答完直接結束回答)'
            },
            "witch-save":{
                "stage_description":"女巫階段，女巫可以使用解藥救狼刀的人",
                "prompt":[
                    f'根據以上綜合資訊，X號玩家死了，請問你要使用解藥並簡述原因？(直接回答"[要或不要]，[原因]"，不需要其他廢話，回答完直接結束回答)',
                ]
            },
            "witch-poison":{
                "stage_description":"女巫階段，女巫可以使用毒藥毒人",
                "prompt":[
                    f'根據以上綜合資訊，請你從{self.alive}號玩家中使用毒藥，或選擇-1表示不使用毒藥，並簡述原因？(直接回答"[玩家]號玩家，[原因]"，不需要其他廢話，回答完直接結束回答)'
                ]
            },
            "dialogue":{
                "stage_description":"玩家發言階段",
                "prompt":'''
                使用JSON的形式來回答，如下所述:
                在這個回答格式中，我希望你能分析多次，以獲得更完整的想法，你要確保你每句話都能以"""裡的內容佐證，不能無中生有。並在[最終的分析]的發言，能夠清楚的表明你的立場，一定要確保發言的正確性，說話的邏輯一定不能有錯誤。
                回答格式:
                {   
                    "分析1": {
                        "想法": "你有甚麼想法?你需要以[你必須知道的資訊]佐證，不能無中生有",
                        "理由": "想出這個想法的理由是甚麼?你需要以[你必須知道的資訊]佐證，不能無中生有",
                        "策略": "有了這個想法，你會怎麼做?",
                        "批評": "對於想法與策略有甚麼可以批評與改進的地方或是有甚麼資訊是你理解錯誤的，請詳細說明",
                    },
                    "分析2": {
                        "反思": "對於前一個想法的批評內容，你能做甚麼改進?你需要以[你必須知道的資訊]佐證，並思考活著玩家可疑的地方，不能無中生有。",
                        "想法": "根據反思，你有甚麼更進一步的想法?你需要以[你必須知道的資訊]佐證，不能無中生有",
                        "理由": "想出這個想法的理由是甚麼?你需要以[你必須知道的資訊]佐證，不能無中生有",
                        "策略": "有了這個想法，你會怎麼做?",
                        "批評": "對於想法與策略有甚麼可以批評與改進的地方或是有甚麼資訊是你理解錯誤的，請詳細說明",
                    }
                    ...(你能夠思考N次，以獲得更完整的發言)
                    "最終的分析":{
                        "反思": "對於前一個想法的批評內容，你能做甚麼改進?你需要以[你必須知道的資訊]佐證，並思考活著玩家可疑的地方，不能無中生有。",
                        "想法": "根據反思，你有甚麼更進一步的想法?你需要以[你必須知道的資訊]佐證，不能無中生有",
                        "理由": "想出這個想法的理由是甚麼?你需要以[你必須知道的資訊]佐證，不能無中生有",
                        "策略": "有了這個想法，你會怎麼做?",
                        "發言": "(請直接呈現你說的話即可，不添加其他附加訊息)"
                    }
                }
                請保證你的回答可以(直接被 Python 的 json.loads 解析)，且你只提供 JSON 格式的回答，不添加其他附加信息。
                '''
            },
            "vote":{
                "stage_description":"白天投票階段，投票最多的人將被票出遊戲",
                "prompt":f'根據以上綜合資訊，請你從{self.alive}號玩家中選一位投票，或選擇-1表示棄票，並簡述原因？(直接回答"[玩家]號玩家，[原因]"，不需要其他廢話，回答完直接結束回答)'
            },
        }
    

        self.init_prompt = f"""你現在正在玩狼人殺，遊戲中玩家會藉由說謊，以獲得勝利。因此，資訊只有玩家發言可能會是假的，而其他的資訊皆是真的
其遊戲設定為{self.room_setting["player_num"]}人局，角色包含{self.room_setting["werewolf"]}位狼人、{self.room_setting["village"]}位平民、{"3" if self.room_setting["hunter"] else "2"}位神職（預言家和女巫{"和獵人" if self.room_setting["hunter"] else ""}）

你是{self.player_id}號玩家，你的角色是{self.user_role}，你的勝利條件為{"殺死所有神職或是所有平民或是狼的數量多於平民加神職的數量" if self.user_role == "wolf" else "殺死所有狼人"}\n\n"""
        
        for x in self.teammate:
            self.init_prompt += f"{x}號玩家是狼，是你的隊友\n"


    def operation(self, stage):

        self.prompt = self.init_prompt

        # information
        self.prompt += f"現在是{self.stage_detail[stage]['stage_description']}\n"
        self.prompt += f"你的資訊為:\n"
        
        if len(self.info) == 0:
            self.prompt += "無資訊\n"
        else: 
            for idx, i in enumerate(self.info):
                self.prompt += f'{idx+1}. {i}\n'
            

        # guess roles
        self.prompt += "\n你猜測玩家的角色：\n"

        if len(self.guess_roles) == 0:
            self.prompt += "無資訊\n"
        else:
            for idx, i in enumerate(self.guess_roles):
                self.prompt += f'{idx}. {i}\n'



        # question
        self.prompt += '\nQ:'
        # self.prompt += '根據以上綜合資訊，0號玩家死了，請問你要使用解藥並簡述原因？(直接回答"[救或不救]，[原因]"，不需要其他廢話)'
        self.prompt += self.stage_detail[stage]['prompt']
        self.prompt += '\nA:'

        # print(self.prompt)
        
        return self.prompt


# room_setting = {
#     "player_num": 6,
#     "operation_time": 10,
#     "dialogue_time": 10,
#     "seer": 1,
#     "witch": 1,
#     "village": 2,
#     "werewolf": 2,
#     "hunter": 0
# }

# p = Prompts(1,room_setting, "witch")
# p.operation('guess-role')