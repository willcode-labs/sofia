import json,re
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db import transaction
from api.apps import ApiConfig
from api.Business.Auth import DecoratorAuth as BusinessDecoratorAuth
from api.Model.Delivery import Delivery as ModelDelivery

class EndPoint(View):
    @csrf_exempt
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def get(self,request,model_login,*args,**kwargs):
        page = request.GET.get('page',None)
        limit = request.GET.get('limit',None)
        delivery_id = request.GET.get('delivery_id',None)
        name = request.GET.get('name',None)
        status = request.GET.get('status',None)

        if delivery_id:
            try:
                model_delivery = ModelDelivery.objects.get(
                    delivery_id=delivery_id,)

            except Exception as error:
                return JsonResponse({'message': 'Registro de entrega não encontrado![130]'}, status=400)

            result = {
                'delivery_id': model_delivery.delivery_id,
                'name': model_delivery.name,
                'description': model_delivery.description,
                'rate': model_delivery.rate,
                'status': model_delivery.status,
            }

            return JsonResponse(result,status=200)

        if page and re.match(r'^[0-9]+$', str(page)) and int(page) >= 1:
            page = int(page)

        else:
            page = 1

        if limit and re.match(r'^[0-9]+$', str(limit)) and int(limit) >= 1:
            limit = int(limit)

        else:
            limit = ApiConfig.query_row_limit

        if status and status not in dict(Delivery.STATUS_LIST).keys():
            raise Exception('Status incorreto![133]')

        try:
            model_delivery = ModelDelivery.objects.filter()

            if name:
                model_delivery = model_delivery.filter(name__icontains=name)

            if status:
                model_delivery = model_delivery.filter(status=status)

        except Exception as error:
            return JsonResponse({'message': 'Registros de entrega não encontrado![131]'}, status=400)

        paginator = Paginator(model_delivery, limit)

        try:
            delivery = paginator.page(page)
            delivery_total = model_delivery.count()
            delivery_has_next = delivery.has_next()
            delivery_has_previous = delivery.has_previous()

            delivery_data = delivery.object_list
            delivery_data = list(delivery_data.values(
                'delivery_id','name','description','rate','status',))

        except Exception as error:
            return JsonResponse({'message': 'Nenhum registro encontrado![132]'}, status=400)

        result = {
            'total': delivery_total,
            'limit': limit,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'has_next': delivery_has_next,
            'has_previous': delivery_has_previous,
            'data': delivery_data,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def post(self,request,model_login,*args,**kwargs):
        try:
            model_delivery = ModelDelivery.objects.create(request,model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'delivery_id': model_delivery.delivery_id,
            'name': model_delivery.name,
            'description': model_delivery.description,
            'rate': model_delivery.status,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def put(self,request,model_login,*args,**kwargs):
        try:
            model_delivery = ModelDelivery.objects.update(request,model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'delivery_id': model_delivery.delivery_id,
            'name': model_delivery.name,
            'description': model_delivery.description,
            'rate': model_delivery.status,
        }

        return JsonResponse(result,status=200)

    @csrf_exempt
    @transaction.atomic
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def delete(self,request,model_login,*args,**kwargs):
        try:
            model_delivery = ModelDelivery.objects.delete(request,model_login)

        except Exception as error:
            return JsonResponse({'message': str(error)}, status=400)

        result = {
            'result': True
        }

        return JsonResponse(result,status=200)

class Price(View):
    @csrf_exempt
    @method_decorator(BusinessDecoratorAuth(profile=('root','director',)))
    def get(self,request,model_login,*args,**kwargs):
        product_list = request.GET.get('product_list',None)
        cep = request.GET.get('cep',None)

        # COD PAC A VISTA 04510
        # COD SEDEX A VISTA 04014

        # http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?
        # nCdEmpresa=&
        # sDsSenha=&
        # nCdServico=04510&
        # sCepOrigem=91750190&
        # sCepDestino=91770100&
        # nVlPeso=3&
        # nCdFormato=1&
        # nVlComprimento=16&
        # nVlAltura=15&
        # nVlLargura=11&
        # nVlDiametro=0&
        # sCdMaoPropria=N&
        # nVlValorDeclarado=45&
        # sCdAvisoRecebimento=N&
        # StrRetorno=XML&
        # nIndicaCalculo=3

        # Retorno
        # <?xml version="1.0" encoding="ISO-8859-1" ?>
        # <Servicos>
        #     <cServico>
        #         <Codigo>04510</Codigo>
        #         <Valor>18,90</Valor>
        #         <PrazoEntrega>7</PrazoEntrega>
        #         <ValorSemAdicionais>18,90</ValorSemAdicionais>
        #         <ValorMaoPropria>0,00</ValorMaoPropria>
        #         <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
        #         <ValorValorDeclarado>0,00</ValorValorDeclarado>
        #         <EntregaDomiciliar>S</EntregaDomiciliar>
        #         <EntregaSabado>N</EntregaSabado>
        #         <Erro>0</Erro>
        #         <MsgErro></MsgErro>
        #         <obsFim></obsFim>
        #     </cServico>
        # </Servicos>

        # Código de erro Mensagem de erro
        # 0 Processamento com sucesso
        # -1 Código de serviço inválido
        # -2 CEP de origem inválido
        # -3 CEP de destino inválido
        # -4 Peso excedido
        # -5 O Valor Declarado não deve exceder R$ 10.000,00
        # -6 Serviço indisponível para o trecho informado
        # -7 O Valor Declarado é obrigatório para este serviço
        # -8 Este serviço não aceita Mão Própria
        # -9 Este serviço não aceita Aviso de Recebimento
        # -10 Precificação indisponível para o trecho informado
        # -11 Para definição do preço deverão ser informados, também, o comprimento, a
        # largura e altura do objeto em centímetros (cm).
        # -12 Comprimento inválido.
        # -13 Largura inválida.
        # -14 Altura inválida.
        # -15 O comprimento não pode ser maior que 105 cm.
        # -16 A largura não pode ser maior que 105 cm.
        # -17 A altura não pode ser maior que 105 cm.
        # -18 A altura não pode ser inferior a 2 cm.
        # -20 A largura não pode ser inferior a 11 cm.
        # -22 O comprimento não pode ser inferior a 16 cm.
        # -23 A soma resultante do comprimento + largura + altura não deve superar a 200 cm.
        # -24 Comprimento inválido.
        # -25 Diâmetro inválido
        # -26 Informe o comprimento.
        # -27 Informe o diâmetro.
        # -28 O comprimento não pode ser maior que 105 cm.
        # -29 O diâmetro não pode ser maior que 91 cm.
        # -30 O comprimento não pode ser inferior a 18 cm.
        # -31 O diâmetro não pode ser inferior a 5 cm.
        # -32 A soma resultante do comprimento + o dobro do diâmetro não deve superar a
        # 200 cm.
        # -33 Sistema temporariamente fora do ar. Favor tentar mais tarde.
        # -34 Código Administrativo ou Senha inválidos.
        # -35 Senha incorreta.
        # -36 Cliente não possui contrato vigente com os Correios.
        # -37 Cliente não possui serviço ativo em seu contrato.
        # -38 Serviço indisponível para este código administrativo.
        # -39 Peso excedido para o formato envelope
        # -40 Para definicao do preco deverao ser informados, tambem, o comprimento e a
        # largura e altura do objeto em centimetros (cm).
        # -41 O comprimento nao pode ser maior que 60 cm.
        # -42 O comprimento nao pode ser inferior a 16 cm.
        # -43 A soma resultante do comprimento + largura nao deve superar a 120 cm.
        # -44 A largura nao pode ser inferior a 11 cm.
        # -45 A largura nao pode ser maior que 60 cm.
        # -888 Erro ao calcular a tarifa
        # 006 Localidade de origem não abrange o serviço informado
        # 007 Localidade de destino não abrange o serviço informado
        # 008 Serviço indisponível para o trecho informado
        # 009 CEP inicial pertencente a Área de Risco.
        # 010 CEP de destino está temporariamente sem entrega domiciliar. A entrega será
        # efetuada na agência indicada no Aviso de Chegada que será entregue no
        # endereço do destinatário
        # 011 CEP de destino está sujeito a condições especiais de entrega pela ECT e será
        # realizada com o acréscimo de até 7 (sete) dias úteis ao prazo regular.
        # 7 Serviço indisponível, tente mais tarde
        # 99 Outros erros diversos do .Net

        result = {
            'price': 0.0
        }

        return JsonResponse(result,status=200)
