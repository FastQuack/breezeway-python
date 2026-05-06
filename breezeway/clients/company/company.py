from typing import TYPE_CHECKING

from breezeway.models.company import Company, Subdepartment, Template

if TYPE_CHECKING:
    from breezeway.breezeway import BreezewayClient, AsyncBreezewayClient

class CompanyClient:
    def __init__(self, client: BreezewayClient):
        self._client = client

    def list_all(self) -> list[Company]:
        """Get all companies associated with the client."""
        request = self._client.resource.company.list_companies()
        companies = self._client.process_request(request)
        return [Company.model_validate(company) for company in companies]

    def subdepartments(self, *, company_id: int | None = None, reference_company_id: int | None = None) -> list[Subdepartment]:
        """
        Provides a list of subdepartments for the specified company.
        Creation of subdepartments can only be performed in the application.
        """
        request = self._client.resource.company.list_subdepartments(company_id=company_id, reference_company_id=reference_company_id)
        subdepartments = self._client.process_request(request)
        return [Subdepartment.model_validate(subdepartment) for subdepartment in subdepartments]

    def templates(self, *, company_id: int | None = None) -> list[Template]:
        """
        Provides a list of templates for the specified company.
        Creation of templates can only be performed in the application.
        """
        request = self._client.resource.company.list_templates(company_id=company_id)
        templates = self._client.process_request(request)
        return [Template.model_validate(template) for template in templates]


class AsyncCompanyClient:
    def __init__(self, client: AsyncBreezewayClient):
        self._client = client

    async def list_all(self) -> list[Company]:
        """Get all companies associated with the client."""
        request = self._client.resource.company.list_companies()
        companies = await self._client.process_request(request)
        return [Company.model_validate(company) for company in companies]

    async def subdepartments(self, *, company_id: int | None = None, reference_company_id: int | None = None) -> list[Subdepartment]:
        """
        Provides a list of subdepartments for the specified company.
        Creation of subdepartments can only be performed in the application.
        """
        request = self._client.resource.company.list_subdepartments(company_id=company_id, reference_company_id=reference_company_id)
        subdepartments = await self._client.process_request(request)
        return [Subdepartment.model_validate(subdepartment) for subdepartment in subdepartments]

    async def templates(self, *, company_id: int | None = None) -> list[Template]:
        """
        Provides a list of templates for the specified company.
        Creation of templates can only be performed in the application.
        """
        request = self._client.resource.company.list_templates(company_id=company_id)
        templates = await self._client.process_request(request)
        return [Template.model_validate(template) for template in templates]
