#!/usr/bin/env python3
# coaching.py - Módulo de Coaching Pessoal
# Perfis de bilionários, mentoria e desenvolvimento pessoal

import json
import random
from datetime import datetime

class CoachingAI:
    """
    IA de Coaching Pessoal
    - Perfis de bilionários e suas estratégias
    - Mentoria personalizada
    - Planos de ação
    - Acompanhamento de metas
    """
    
    def __init__(self):
        self.billionaires = self.load_billionaire_profiles()
        self.user_profile = {}
        self.goals = []
        self.habits = []
        
        print("[Coaching] 🎯 IA de Coaching inicializada")
    
    def load_billionaire_profiles(self):
        """Carrega perfis de bilionários e suas estratégias."""
        return {
            'warren_buffett': {
                'name': 'Warren Buffett',
                'net_worth': '120 bilhões',
                'industry': 'Investimentos',
                'key_principles': [
                    'Invista em empresas que você entende',
                    'Pense a longo prazo',
                    'Seja paciente e disciplinado',
                    'Aprenda continuamente',
                    'Viva abaixo das suas possibilidades'
                ],
                'daily_habits': [
                    'Ler 500 páginas por dia',
                    'Focar em decisões de longo prazo',
                    'Evitar dívidas',
                    'Investir em conhecimento'
                ],
                'quotes': [
                    'O mercado é um dispositivo para transferir dinheiro do impaciente para o paciente',
                    'Preço é o que você paga, valor é o que você recebe',
                    'Seja ganancioso quando os outros têm medo'
                ]
            },
            'elon_musk': {
                'name': 'Elon Musk',
                'net_worth': '250 bilhões',
                'industry': 'Tecnologia/Espaço',
                'key_principles': [
                    'Pense grande e ouse',
                    'Trabalhe incansavelmente',
                    'Resolva problemas impossíveis',
                    'Aprenda com primeiros princípios',
                    'Não tenha medo de falhar'
                ],
                'daily_habits': [
                    'Trabalhar 80-100 horas por semana',
                    'Dividir tempo em blocos de 5 minutos',
                    'Focar em física e engenharia',
                    'Questionar tudo'
                ],
                'quotes': [
                    'Quando algo é importante o suficiente, você faz mesmo que as chances não estejam a seu favor',
                    'Falhar é uma opção aqui. Se as coisas não estão falhando, você não está inovando o suficiente',
                    'Eu acho que é possível para pessoas comuns escolherem ser extraordinárias'
                ]
            },
            'jeff_bezos': {
                'name': 'Jeff Bezos',
                'net_worth': '180 bilhões',
                'industry': 'E-commerce/Tecnologia',
                'key_principles': [
                    'Seja obcecado pelo cliente',
                    'Invente e simplifique',
                    'Tenha visão de longo prazo',
                    'Tome decisões de alta qualidade',
                    'Contrate e desenvolva os melhores'
                ],
                'daily_habits': [
                    'Dormir 8 horas',
                    'Fazer decisões importantes de manhã',
                    'Ter reuniões pequenas',
                    'Experimentar constantemente'
                ],
                'quotes': [
                    'Sua margem é minha oportunidade',
                    'Nós somos teimosos em visão e flexíveis em detalhes',
                    'Se você nunca quer estar errado, você nunca vai dizer algo original'
                ]
            },
            'bill_gates': {
                'name': 'Bill Gates',
                'net_worth': '130 bilhões',
                'industry': 'Tecnologia/Filantropia',
                'key_principles': [
                    'Aprenda constantemente',
                    'Seja apaixonado pelo que faz',
                    'Cerque-se de pessoas inteligentes',
                    'Dê retorno à sociedade',
                    'Pense no impacto de longo prazo'
                ],
                'daily_habits': [
                    'Ler 50 livros por ano',
                    'Pensar profundamente',
                    'Fazer anotações',
                    'Discutir ideias'
                ],
                'quotes': [
                    'Seu cliente mais insatisfeito é sua maior fonte de aprendizado',
                    'Sucesso é um péssimo professor. Ele seduz pessoas inteligentes a pensar que não podem perder',
                    'Nós sempre superestimamos a mudança que ocorrerá nos próximos dois anos e subestimamos a mudança que ocorrerá nos próximos dez'
                ]
            },
            'mark_cuban': {
                'name': 'Mark Cuban',
                'net_worth': '5 bilhões',
                'industry': 'Investimentos/Esportes',
                'key_principles': [
                    'Trabalhe mais que todos',
                    'Aprenda continuamente',
                    'Venda, venda, venda',
                    'Seja persistente',
                    'Ame o que você faz'
                ],
                'daily_habits': [
                    'Estudar 3 horas por dia',
                    'Estar sempre aprendendo',
                    'Networking constante',
                    'Tomar riscos calculados'
                ],
                'quotes': [
                    'Não siga suas paixões, siga seu esforço',
                    'Todo mundo tem um talento. O que é raro é a coragem de seguir para onde ele te leva',
                    'Trabalhe como se alguém estivesse trabalhando 24 horas por dia para tirar tudo de você'
                ]
            }
        }
    
    def get_random_billionaire(self):
        """Retorna um bilionário aleatório."""
        key = random.choice(list(self.billionaires.keys()))
        return self.billionaires[key]
    
    def get_daily_inspiration(self):
        """Retorna inspiração diária de um bilionário."""
        billionaire = self.get_random_billionaire()
        quote = random.choice(billionaire['quotes'])
        
        return {
            'billionaire': billionaire['name'],
            'quote': quote,
            'principle': random.choice(billionaire['key_principles']),
            'habit': random.choice(billionaire['daily_habits'])
        }
    
    def create_action_plan(self, goal, timeframe='30 dias'):
        """Cria plano de ação baseado em estratégias de bilionários."""
        # Selecionar bilionário relevante
        billionaire = self.get_random_billionaire()
        
        # Criar plano
        plan = {
            'goal': goal,
            'timeframe': timeframe,
            'mentor': billionaire['name'],
            'strategy': billionaire['key_principles'][0],
            'daily_actions': [],
            'weekly_milestones': [],
            'success_metrics': []
        }
        
        # Ações diárias baseadas em hábitos de bilionários
        daily_actions = [
            'Acordar às 5:00 AM',
            'Ler 1 hora sobre o tema',
            'Trabalhar 2 horas no objetivo',
            'Fazer networking com 1 pessoa',
            'Revisar progresso do dia'
        ]
        
        plan['daily_actions'] = daily_actions
        
        # Marcos semanais
        weeks = int(timeframe.split()[0]) // 7
        for i in range(1, weeks + 1):
            plan['weekly_milestones'].append(f'Semana {i}: Completar {i*25}% do objetivo')
        
        # Métricas de sucesso
        plan['success_metrics'] = [
            'Progresso mensurável diário',
            'Hábitos consistentes',
            'Resultados tangíveis',
            'Aprendizado documentado'
        ]
        
        return plan
    
    def analyze_mindset(self, responses):
        """Analisa mindset do usuário."""
        # Perguntas e análise
        mindset_score = {
            'growth': 0,
            'resilience': 0,
            'discipline': 0,
            'vision': 0,
            'action': 0
        }
        
        # Análise simplificada
        for key in mindset_score:
            mindset_score[key] = random.uniform(0.5, 1.0)
        
        # Identificar bilionário mais similar
        avg_score = sum(mindset_score.values()) / len(mindset_score)
        
        if avg_score > 0.8:
            similar_to = 'elon_musk'
        elif avg_score > 0.7:
            similar_to = 'jeff_bezos'
        elif avg_score > 0.6:
            similar_to = 'warren_buffett'
        else:
            similar_to = 'bill_gates'
        
        return {
            'scores': mindset_score,
            'overall': avg_score,
            'similar_to': self.billionaires[similar_to]['name'],
            'recommendations': self.get_recommendations(mindset_score)
        }
    
    def get_recommendations(self, mindset_score):
        """Gera recomendações baseadas no mindset."""
        recommendations = []
        
        for trait, score in mindset_score.items():
            if score < 0.7:
                if trait == 'growth':
                    recommendations.append('Desenvolver mentalidade de crescimento - ler "Mindset" de Carol Dweck')
                elif trait == 'resilience':
                    recommendations.append('Fortalecer resiliência - praticar meditação e exercícios')
                elif trait == 'discipline':
                    recommendations.append('Aumentar disciplina - criar rotina matinal rígida')
                elif trait == 'vision':
                    recommendations.append('Clarificar visão - definir metas de 5, 10 e 20 anos')
                elif trait == 'action':
                    recommendations.append('Aumentar ação - aplicar regra dos 5 segundos de Mel Robbins')
        
        return recommendations
    
    def generate_morning_routine(self, billionaire_key=None):
        """Gera rotina matinal baseada em bilionário."""
        if not billionaire_key:
            billionaire_key = random.choice(list(self.billionaires.keys()))
        
        billionaire = self.billionaires[billionaire_key]
        
        routine = {
            'name': f'Rotina {billionaire["name"]}',
            'duration': '2 horas',
            'activities': []
        }
        
        # Rotina genérica inspirada
        activities = [
            {'time': '05:00', 'activity': 'Acordar', 'duration': '5 min'},
            {'time': '05:05', 'activity': 'Meditação/Reflexão', 'duration': '15 min'},
            {'time': '05:20', 'activity': 'Exercício físico', 'duration': '30 min'},
            {'time': '05:50', 'activity': 'Banho frio', 'duration': '10 min'},
            {'time': '06:00', 'activity': 'Café da manhã saudável', 'duration': '20 min'},
            {'time': '06:20', 'activity': 'Leitura/Estudo', 'duration': '40 min'},
            {'time': '07:00', 'activity': 'Planejamento do dia', 'duration': '20 min'}
        ]
        
        routine['activities'] = activities
        routine['key_principle'] = billionaire['key_principles'][0]
        
        return routine
    
    def track_progress(self, goal_id, progress_data):
        """Acompanha progresso de uma meta."""
        # Análise de progresso
        analysis = {
            'goal_id': goal_id,
            'completion': progress_data.get('completion', 0),
            'consistency': progress_data.get('consistency', 0),
            'obstacles': progress_data.get('obstacles', []),
            'wins': progress_data.get('wins', []),
            'next_actions': []
        }
        
        # Gerar próximas ações
        if analysis['completion'] < 0.25:
            analysis['next_actions'].append('Revisar estratégia - pode estar muito ambiciosa')
            analysis['next_actions'].append('Quebrar em tarefas menores')
        elif analysis['completion'] < 0.5:
            analysis['next_actions'].append('Manter consistência')
            analysis['next_actions'].append('Celebrar pequenas vitórias')
        elif analysis['completion'] < 0.75:
            analysis['next_actions'].append('Acelerar execução')
            analysis['next_actions'].append('Buscar mentoria')
        else:
            analysis['next_actions'].append('Finalizar com excelência')
            analysis['next_actions'].append('Preparar próximo objetivo')
        
        return analysis
    
    def get_book_recommendations(self, area='geral'):
        """Recomenda livros por área."""
        books = {
            'geral': [
                'Mindset - Carol Dweck',
                'Hábitos Atômicos - James Clear',
                'O Poder do Hábito - Charles Duhigg',
                'Pense e Enriqueça - Napoleon Hill',
                'Os 7 Hábitos das Pessoas Altamente Eficazes - Stephen Covey'
            ],
            'negocios': [
                'De Zero a Um - Peter Thiel',
                'A Startup Enxuta - Eric Ries',
                'Empresas Feitas para Vencer - Jim Collins',
                'O Dilema da Inovação - Clayton Christensen',
                'Trabalhe 4 Horas por Semana - Tim Ferriss'
            ],
            'investimentos': [
                'O Investidor Inteligente - Benjamin Graham',
                'Pai Rico, Pai Pobre - Robert Kiyosaki',
                'Os Segredos da Mente Milionária - T. Harv Eker',
                'A Psicologia Financeira - Morgan Housel',
                'Ações Comuns, Lucros Extraordinários - Philip Fisher'
            ],
            'produtividade': [
                'Foco - Daniel Goleman',
                'Trabalho Focado - Cal Newport',
                'A Regra dos 5 Segundos - Mel Robbins',
                'Essencialismo - Greg McKeown',
                'O Poder do Agora - Eckhart Tolle'
            ]
        }
        
        return books.get(area, books['geral'])
    
    def print_daily_coaching(self):
        """Imprime coaching diário."""
        inspiration = self.get_daily_inspiration()
        
        print("\n" + "="*60)
        print("[Coaching] 🎯 COACHING DIÁRIO")
        print("="*60)
        print(f"\n💡 Mentor do Dia: {inspiration['billionaire']}")
        print(f"\n📖 Citação:")
        print(f'   "{inspiration["quote"]}"')
        print(f"\n🎯 Princípio:")
        print(f"   {inspiration['principle']}")
        print(f"\n✅ Hábito para Hoje:")
        print(f"   {inspiration['habit']}")
        print("\n" + "="*60)


# Teste
if __name__ == "__main__":
    coach = CoachingAI()
    
    # Inspiração diária
    coach.print_daily_coaching()
    
    # Criar plano de ação
    print("\n")
    plan = coach.create_action_plan('Ganhar R$ 10.000/mês', '90 dias')
    print(f"Plano de Ação: {plan['goal']}")
    print(f"Mentor: {plan['mentor']}")
    print(f"Estratégia: {plan['strategy']}")
    
    # Rotina matinal
    print("\n")
    routine = coach.generate_morning_routine()
    print(f"Rotina: {routine['name']}")
    for act in routine['activities'][:3]:
        print(f"  {act['time']} - {act['activity']}")

