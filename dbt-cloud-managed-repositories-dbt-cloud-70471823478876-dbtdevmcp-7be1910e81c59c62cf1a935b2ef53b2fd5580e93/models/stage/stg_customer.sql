with 

source as (

    select * from {{ ref('raw_customer') }}

),

renamed as (

    select
        c_custkey as customer_key,
        c_name as name,
        c_address as address,
        c_nationkey as nation_key,
        c_phone as phone,
        c_acctbal as account_balance,
        c_mktsegment as marketing_segment,
        c_comment as comment

    from source

)

select * from renamed