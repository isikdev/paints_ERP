from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.pg_extension import PGExtension
from alembic_utils.pg_view import PGView

pgcrypto_extension = PGExtension(
    schema="public",
    signature="pgcrypto",
)

increment_document_number = PGFunction(
    schema="public",
    signature="increment_document_number()",
    definition="""
    RETURNS trigger AS
    $$
    DECLARE
        current_year INTEGER := EXTRACT(YEAR FROM NEW.document_datetime);
        new_counter INTEGER;
    BEGIN
        -- вставляем новую строку в счётчик (стартуя с 1) или увеличиваем существующий
        INSERT INTO document_number_counters (id, document_type_id, year, counter)
        VALUES (gen_random_uuid(), NEW.document_type_id, current_year, 1)
        ON CONFLICT (document_type_id, year)
        DO UPDATE SET counter = document_number_counters.counter + 1
        RETURNING counter INTO new_counter;

        -- проставляем в новый документ номер и шаблонное имя
        NEW.document_number := new_counter;

        IF NEW.name IS NULL OR NEW.name = '' THEN
            NEW.name := format(
                'document%s_%s',
                lpad(new_counter::TEXT, 3, '0'),
                current_year
            );
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
)

set_document_number_trigger_base_recipes = PGTrigger(
    schema="public",
    signature="set_document_number_base_recipes",
    on_entity="base_recipes",
    definition="""
    BEFORE INSERT ON base_recipes
    FOR EACH ROW
    EXECUTE FUNCTION increment_document_number();
    """
)

set_document_number_trigger_documents = PGTrigger(
    schema="public",
    signature="set_document_number_documents",
    on_entity="documents",
    definition="""
    BEFORE INSERT ON documents
    FOR EACH ROW
    EXECUTE FUNCTION increment_document_number();
    """
)

stock_balance_view = PGView(
    schema="public",
    signature="stock_balance",
    definition="""
    SELECT m.nomenclature_id, n.type_id AS item_type_id, SUM(m.qty) AS balance
    FROM stock_moves m
    JOIN nomenclatures n ON n.id = m.nomenclature_id
    GROUP BY m.nomenclature_id, n.type_id;
    """
)

get_stock_balance_function = PGFunction(
    schema="public",
    signature="get_stock_balance(p_nomenclature_id uuid)",
    definition="""
    RETURNS numeric AS $$
    SELECT COALESCE(SUM(qty), 0)
      FROM stock_moves
     WHERE nomenclature_id = p_nomenclature_id;
    $$ LANGUAGE SQL STABLE;
    """
)
