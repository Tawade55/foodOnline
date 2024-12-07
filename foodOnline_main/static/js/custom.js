let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
}
//Add to cart
$(document).ready(function(){                   //hyat na aata jeva pan + var cart madhe click karnaar teva food id ani tyacha url store honaar
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        
        food_id=$(this).attr('data-id');
        url=$(this).attr('data-url');

        
        $.ajax({                                //ajax vaparla karanki aaplya la cart madhe add kartana reloading nakoy direct disla paije
            type:'GET',                         //ajax get req ne url ani food id ghetoy
            url:url,
           
            success:function(response){
                console.log(response)
                if(response.status=="login_required"){
                    swal(response.message,'','info').then(function(){
                        window.location='/accounts/login';
                    })
                     
                }else if(response.status=="Failed"){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    //subtotal,tax and grand_total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
                    )

                }

            }
        })
    })



//place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id=$(this).attr('id')
        var qty=$(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
    //decrease cart
    $('.decrease_cart').on('click',function(e){
            e.preventDefault();
            
            food_id=$(this).attr('data-id');
            url=$(this).attr('data-url');
    
            
            $.ajax({                                //ajax vaparla karanki aaplya la cart madhe add kartana reloading nakoy direct disla paije
                type:'GET',                         //ajax get req ne url ani food id ghetoy
                url:url,
                
                success:function(response){
                    console.log(response)
                    if(response.status=="login_required"){
                        swal(response.message,'','info').then(function(){
                            window.location='/accounts/login';
                        })
                         
                    }
                    else if(response.status=="Failed"){
                        swal(response.message,'','error')
                    }else{
                        $('#cart_counter').html(response.cart_counter['cart_count']);
                        $('#qty-'+food_id).html(response.qty);

                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax_dict'],
                            response.cart_amount['grand_total'],
                        )
    
                    }
                    
                }
            })
        })
        // delete cart
        $('.delete_cart').on('click',function(e){
            e.preventDefault();

            
            
            cart_id=$(this).attr('data-id');
            url=$(this).attr('data-url');
    
            
            $.ajax({                                //ajax vaparla karanki aaplya la cart madhe add kartana reloading nakoy direct disla paije
                type:'GET',                         //ajax get req ne url ani food id ghetoy
                url:url,
                
                success:function(response){
                    console.log(response)
                    if(response.status=="Failed"){
                        swal(response.message,'','error')
                    }else{
                        $('#cart_counter').html(response.cart_counter['cart_count']);
                        swal(response.status,response.message,"success")

                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax_dict'],
                            response.cart_amount['grand_total'],
                        )
                        
                        removeCartItem(0,cart_id);
                        checkEmptyCart();
                    }
                    
                }
            })
        })

        //delete the cart element if the qty is 0
        function removeCartItem(cartItemQty,cart_id){
            if(cartItemQty<=0){
                //remove the cart item element
                document.getElementById("cart-item-"+cart_id).remove()
            }
        }
        function checkEmptyCart(){
            var cart_counter=document.getelementById('cart_counter').innerHTML
            if(cart_counter==0){
                document.getElementById("empty-cart").style.display="block";
            }
        }

        //Apply cart amounts
        function applyCartAmounts(subtotal,tax_dict,grand_total){
            if(window.location.pathname=='/cart/'){ //heh fakta user logedin aasel ar tyala disla paije
                $('#subtotal').html(subtotal)   //ikde aapan html code madhun id fetch keli aahe ani tila ikdun call karat aahe tikde render karnya sathi
                $('#total').html(grand_total)

                console.log(tax_dict)
                for(key1 in tax_dict){
                    console.log(tax_dict[key1])
                    for(key2 in tax_dict[key1]){
                        //console.log(tax_dict[key1][key2])
                        $('#tax-'+key1).html(tax_dict[key1][key2])
                    }
                }
            }
        }
});

