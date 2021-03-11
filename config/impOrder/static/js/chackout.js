const IMP = window.IMP;
IMP.init('imp77590125');

$(document).ready(function() {
    $('#payment-form').on('submit', function (e) {
  
        e.preventDefault();
        alert('KG 이니시스 정책상 11:00PM 자동 결제 취소됩니다.\nThe payment will be canceled at 11:00PM korean time');

        // const amount = $('#amount').data('amount').toString().replace('.', '');
        const amount = 100;

        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
        const email = document.getElementById('email').value;
        const address = document.getElementById("address").value;
        const zip_code = document.getElementById("zip_code").value;
        const count = document.getElementsByName("phone_number").length;
        const phone_array = new Array();
        for (let i = 0; i < count; i++) {
            phone_array.push(document.getElementsByName("phone_number")[i].value);
        }
        phone_number = phone_array.join("-");

        const order_id = AjaxCreateOrder(e, amount);
        if(!order_id){
            alert("주문 실패\n 다시 시도해 주세요.");
            // 폼이 중단함 True이면 전송 해버림 
            return false; 
        }


        const merchant_id = AjaxStoreTransaction(e, order_id, amount);
        if(merchant_id) {
            IMP.request_pay({
                //요청
                merchant_uid: merchant_id,
                name: 'Stay Gold Pament Test (결제 테스트)',
                // buyer_name:first_name + " " + last_name,
                buyer_email:email,
                amount : amount, 
                // buyer_tel : phone_number,
                // buyer_addr :address,
                // buyer_postcode:zip_code,
            }, function(response) {
                //완료된 이후
                if (response.success) { 
                    let msg = '결제가 완료되었습니다.\nPayment success';
                    // msg += '고유ID(ID) : ' + response.imp_uid;
                    // msg += '상점 거래ID(Merchant_ID) : ' + response.merchant_uid;
                    // msg += '결제 금액(Amount) : ' + response.paid_amount;
                    // msg += '카드 승인번호(Apply number) : ' + response.apply_num;
                    // 결제가 완료되었으면 비교해서 디비에 반영
                    
                    ImpTransaction(e, order_id, response.merchant_uid, response.imp_uid, response.paid_amount);
                    alert(msg);
                }
                else {
                    alert('결제실패(Payment Error) : ' + response.error_msg);
                }
            })
        }
        return false;
    })

    // 폼 데이터를 기준으로 주문 생성
    function AjaxCreateOrder(e, amount) {
        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
        const email = document.getElementById('email').value;
        const address = document.getElementById("address").value;
        const zip_code = document.getElementById("zip_code").value;
        const count = document.getElementsByName("phone_number").length;

        const phone_array = new Array();
        for (let i = 0; i < count; i++) {
            phone_array.push(document.getElementsByName("phone_number")[i].value);
        }
        phone_number = phone_array.join("-");

        let order_id = ''
        $.ajax({
            type: "POST",
            url: ORDER_CREATE_URL,
            async: false,
            data: {
                first_name,
                last_name,
                phone_number,
                email,
                address,
                zip_code,
                total_price : amount,
                csrfmiddlewaretoken: CSRF_TOKEN,
            },
            success: function (json) {
                order_id = json.order_id
            },
            error: function (xhr, errmsg, err) {
                if (xhr.status == 404) {
                    alert("페이지가 존재하지 않습니다.");
                } 
                else if (xhr.status == 403) {
                    alert("로그인 해주세요.");
                } 
                else {
                    alert("문제가 발생했습니다. 다시 시도해주세요.");
                }
            }
        });
        return order_id
    }

    // 결제 정보 생성
    function AjaxStoreTransaction(e, order_id, amount) {
        e.preventDefault();
        let merchant_id = '';
        const request = $.ajax({
            method: "POST",
            url: ORDER_CHECKOUT_URL,
            async: false,
            data: {
                order_id,
                amount,
                csrfmiddlewaretoken: CSRF_TOKEN,
            }
        });
        request.done(function (data) {
            if (data.success) {
                merchant_id = data.merchant_id;
            }
        });
        request.fail(function (jqXHR, textStatus) {
            if (jqXHR.status == 404) {
                alert("페이지가 존재하지 않습니다.");
            } else if (jqXHR.status == 403) {
                alert("로그인 해주세요.");
            } else {
                alert("문제가 발생했습니다. 다시 시도해주세요.");
            }
        });
        return merchant_id;
    }
    // iamport에 결제 정보가 있는지 확인 후 결제 완료 페이지로 이동
    function ImpTransaction(e, order_id,merchant_id, imp_id, amount) {
        e.preventDefault();
        var request = $.ajax({
            method: "POST",
            url: ORDER_VALIDATION_URL,
            async: false,
            data: {
                order_id:order_id,
                merchant_id: merchant_id,
                imp_id: imp_id,
                amount: amount,
                csrfmiddlewaretoken: CSRF_TOKEN,
            }
        });
        request.done(function (data) {
            if (data.success) {
                window.location.replace(PAYMENT_SUCCESS_URL);
                // $(location).attr('href', location.origin + ORDER_COMPLETE_URL + '?order_id='+order_id)
            }
        });
        request.fail(function (jqXHR, textStatus) {
            if (jqXHR.status == 404) {
                alert("페이지가 존재하지 않습니다.");
            } else if (jqXHR.status == 403) {
                alert("로그인 해주세요.");
            } else {
                alert("문제가 발생했습니다. 다시 시도해주세요.");
            }
        });
    }
});
